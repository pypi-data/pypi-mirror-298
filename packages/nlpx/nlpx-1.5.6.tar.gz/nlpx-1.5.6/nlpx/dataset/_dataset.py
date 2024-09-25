import torch
import numpy as np
import pandas as pd
from typing import Union, List, Tuple
from torch.utils.data import Dataset

from nlpx.llm import TokenizeVec
from nlpx.text_token import BaseTokenizer, TokenEmbedding
from nlpx.text_token.utils import get_texts_max_length


class ListDataset(Dataset[Tuple[List, ...]]):
	r"""Dataset wrapping List.

	Each sample will be retrieved by indexing list.

	Args:
		*lists (List): lists that have the same length.
	"""
	
	lists: Tuple[List, ...]
	
	def __init__(self, *lists: List) -> None:
		assert all(len(lists[0]) == len(sub_list) for sub_list in lists), "Size mismatch between tensors"
		self.lists = lists
	
	def __getitem__(self, index):
		if len(self.lists) == 1:
			return self.lists[0][index]
		return tuple(sub_list[index] for sub_list in self.lists)
	
	def __len__(self):
		return len(self.lists[0])


class TokenDataset(Dataset):
	""" Token的长度不一样
	返回的是(token, label) 不是Tensor, 必须经过PaddingTokenCollator
	"""
	
	def __init__(self, tokens: Union[List[int], np.ndarray],
	             labels: Union[List, np.ndarray, pd.Series]):
		super().__init__()
		self.tokens = tokens
		self.labels = labels.values if isinstance(labels, pd.Series) else labels
	
	def __getitem__(self, index: int):
		return self.tokens[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class SameLengthTokenDataset(Dataset):
	""" Token已经truncate和padding, 长度一样
	返回的是Tensor, 不需要经过collate_fn
	"""
	
	def __init__(self, tokens: Union[List[int], np.ndarray, torch.LongTensor],
	             labels: Union[List, np.ndarray, pd.Series, torch.LongTensor]):
		super().__init__()
		self.tokens = tokens if isinstance(tokens, torch.LongTensor) else torch.tensor(tokens, dtype=torch.long)
		labels = labels.values if isinstance(labels, pd.Series) else labels
		self.labels = labels if isinstance(labels, torch.LongTensor) else torch.tensor(labels, dtype=torch.long)
	
	def __getitem__(self, index: int):
		return self.tokens[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class TextDataset(Dataset):
	""" 返回的是(text, label) 不是Tensor, 必须经过TextVecCollator """
	
	def __init__(self, texts: Union[List[str], np.ndarray, pd.Series], labels: Union[List, np.ndarray, pd.Series]):
		super().__init__()
		self.texts = texts.values if isinstance(texts, pd.Series) else texts
		self.labels = labels.values if isinstance(labels, pd.Series) else labels
	
	def __getitem__(self, index: int):
		return self.texts[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class TextDFDataset(Dataset):
	""" 返回的是(text, label) 不是Tensor, 必须经过TextVecCollator """
	
	def __init__(self, data_df: pd.DataFrame):
		"""
		:param data_df: 只有两列 ['text', 'label'], 注意顺序，第一列是text, 第二列是label
		"""
		super().__init__()
		self.data = data_df.values
	
	def __getitem__(self, index: int):
		return self.data[index]
	
	def __len__(self):
		return len(self.data)


class TextVecCollator:
	
	def __init__(self, tokenize_vec: Union[TokenizeVec, TokenEmbedding], max_length: int = None, **kwargs):
		self.tokenize_vec = tokenize_vec
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples):
		texts, labels = zip(*examples)
		labels = torch.tensor(np.array(labels), dtype=torch.long)
		
		if isinstance(self.tokenize_vec, TokenizeVec):
			max_length = get_texts_max_length(texts, cut_type='char') + 2
			max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
			return self.tokenize_vec.encode_plus(texts, max_length=max_length, padding='max_length',
			                                     truncation=True, add_special_tokens=True,
			                                     return_token_type_ids=True, return_attention_mask=True,
			                                     return_tensors='pt', **self.kwargs), labels
		elif isinstance(self.tokenize_vec, TokenEmbedding):
			max_length = get_texts_max_length(texts, cut_type=self.tokenize_vec.cut_type,
			                                  lang=self.tokenize_vec.lang, cut_fn=self.tokenize_vec.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
			return self.tokenize_vec(texts, max_length, **self.kwargs), labels
		
		raise ValueError("Invalid tokenize_vec, it must be a TokenizeVec or TokenEmbedding.")


class TokenizeCollator:
	
	def __init__(self, tokenizer, max_length: int = None, **kwargs):
		self.tokenizer = tokenizer
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples):
		texts, labels = zip(*examples)
		labels = torch.tensor(np.array(labels), dtype=torch.long)
		
		if isinstance(self.tokenizer, BaseTokenizer):
			max_length = get_texts_max_length(texts, cut_type=self.tokenizer.cut_type, lang=self.tokenizer.lang,
			                                  cut_fn=self.tokenizer.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length else max_length
			return torch.tensor(self.tokenizer.batch_encode(texts, max_length, **self.kwargs), dtype=torch.long), labels
		
		max_length = get_texts_max_length(texts, cut_type='char') + 2
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		result = self.tokenizer.batch_encode_plus(texts, max_length=max_length, padding='max_length',
		                                          return_token_type_ids=True, return_attention_mask=True,
		                                          truncation=True, add_special_tokens=True, return_tensors='pt',
		                                          **self.kwargs)
		result['labels'] = labels
		return result


class PaddingTokenCollator:
	"""与TokenDataset配合使用
	
	Examples
	--------
	>>> tokenizer = PaddingTokenizer(texts=texts)
	>>> X_train = tokenizer.batch_encode(texts, padding=False)
	>>> train_set = TokenDataset(X_train, y_train)
	>>> model_wrapper = ClassModelWrapper(classes=classes)
	>>> model_wrapper.train(model, train_set, early_stopping_rounds=5, show_progress=False,
	>>>                     collate_fn=PaddingTokenCollator(tokenizer.pad, return_sequence_length=True))
	"""
	
	def __init__(self, pad_func, max_length: int = None, truncation=True, padding_side='right',
	             return_sequence_length=False, bos=False, eos=False):
		self.pad_func = pad_func
		self.max_length = max_length
		self.truncation = truncation
		self.padding_side = padding_side
		self.return_sequence_length = return_sequence_length
		self.bos, self.eos = bos, eos
	
	def __call__(self, examples):
		tokens, labels = zip(*examples)
		labels = torch.tensor(np.array(labels), dtype=torch.long)
		
		max_length = max(map(lambda x: len(x), tokens))
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		params = {'truncation': self.truncation, 'padding_side': self.padding_side}
		if self.bos:
			params['bos'] = self.bos
		if self.eos:
			params['eos'] = self.eos
		
		if self.return_sequence_length:
			params['return_sequence_length'] = self.return_sequence_length
			ids, sequence_lengths = self.pad_func(tokens, max_length, **params)
			return torch.tensor(ids, dtype=torch.long), torch.tensor(sequence_lengths, dtype=torch.int), labels
		
		ids = self.pad_func(tokens, max_length, **params)
		if isinstance(ids, Tuple):
			ids = ids[0]
		return torch.tensor(ids, dtype=torch.long), labels
