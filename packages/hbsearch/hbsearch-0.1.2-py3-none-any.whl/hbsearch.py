import argparse
from collections import defaultdict
from FlagEmbedding import FlagReranker
from rank_bm25 import BM25Okapi
import jieba

def reciprocal_rank_fusion(*list_of_list_ranks_system, K=60):
    # Dictionary to store RRF mapping
    rrf_map = defaultdict(float)

    # Calculate RRF score for each result in each list
    for rank_list in list_of_list_ranks_system:
        for rank, item in enumerate(rank_list, 1):
            rrf_map[item] += 1 / (rank + K)

    # Sort items based on their RRF scores in descending order
    sorted_items = sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)

    # Return tuple of list of sorted documents by score and sorted documents
    return sorted_items, [item for item, _ in sorted_items]


def chunkstring(doc_string, length):
  # Chunk preprocessing
  chunks = []
  i, c = 0, 0
  while i + length < len(doc_string):
    end = i + length
    while end + c < len(doc_string) and doc_string[end + c].encode().isalpha():
      c = c + 1
    chunks.append(doc_string[i:end + c])
    i = i + length + c
    c = 0
  if i < len(doc_string): chunks.append(doc_string[i:])
  return chunks

def semantic_rank(query, chunks):
  # Semantic search
  reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True) # Setting use_fp16 to True s
  semantic_scores = reranker.compute_score([[query, p] for p in chunks], normalize=True)
  return semantic_scores

def bm25_rank(query, chunks):
  # Match search
  tokenized_corpus = [list(jieba.cut_for_search(doc)) for doc in chunks]
  bm25 = BM25Okapi(tokenized_corpus)
  bm25_scores = bm25.get_scores(list(jieba.cut_for_search(query)))
  return bm25_scores

def hybird_search(query, doc_string, chunk_size=1000):
  # Two-way recall
  chunks = chunkstring(doc_string, chunk_size)
  semantic_scores = semantic_rank(query, chunks)
  bm25_scores = bm25_rank(query, chunks)
  result_1 = list(zip(chunks, semantic_scores))
  result_2 = list(zip(chunks, bm25_scores))
  sorted_result_1 = sorted(result_1, key=lambda x:x[1], reverse=True)
  sorted_result_2 = sorted(result_2, key=lambda x:x[1], reverse=True)

  return reciprocal_rank_fusion([x[0] for x in sorted_result_1],
                                  [x[0] for x in sorted_result_2])

def hybird_search_top_k(query, doc_string, topk=5, chunk_size=1000):
  return hybird_search(query, doc_string, chunk_size)[0][0:topk]

if __name__=='__main__':

  toy_corpus = [
    "精确模式，试图将句子最精确地切开，适合文本分析；",
    "全模式，把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；",
    "搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。",
    "I am from China, I like math."
  ]
  toy_doc_string = (
    '精确模式，试图将句子最精确地切开，适合文本分析；全模式，'
    '把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；'
    '搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。'
    'I am from China, I like math.'
  )
  toy_query = "模式"

  toy_string = "aaaaefasdf askdfjlasjd"
  parser = argparse.ArgumentParser(description='chunk hybrid search.')
  parser.add_argument('-f','--file', metavar='file', help='Specify a text file')
  parser.add_argument('-q','--query', metavar='query', default='做好房屋体检确保居住安全',
                      help='query for search')
  parser.add_argument('-s','--chunk_size', metavar='chunk_size', default=1000,
                      type=int, help='chunk size')
  parser.add_argument('-v','--verbose', action='store_true', default=False,
                      help='print the process in detail')
  parser.add_argument('-t','--toy', action='store_true', default=False,
                      help='execute the toy example')
  args = parser.parse_args()

  if args.toy:
    print(bm25_rank(toy_query, toy_corpus))
    print(semantic_rank(toy_query, toy_corpus))
    print(hybird_search(toy_query, toy_doc_string, 10))
    parser.print_help()
    exit(0)
  if args.file is None:
    print("Please specify the text file path")
    parser.print_help()
    exit(0)
  # filename= 'data/pdfout/95a229e1-3c34-4d06-bdaa-25298ae5fe8e/auto/95a229e1-3c34-4d06-bdaa-25298ae5fe8e.md'
  text =open(args.file, 'r').read().strip('\n')
  result = hybird_search_top_k('做好房屋体检确保居住安全', text, 1000)
  print(result)
