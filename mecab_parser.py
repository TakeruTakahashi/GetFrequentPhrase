#!usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import MeCab

# 分かち書きの単語リストと単語と品詞のディクショナリを返す
def get_parsed_words_dict(input_text):
    t=MeCab.Tagger("-Owakati")
    tagger=MeCab.Tagger("mecabrc")
    text=input_text.encode("utf-8")
    node=tagger.parseToNode(text)

    words=[]        # 分かち書きの単語リスト
    pos_dict={}     # 単語と品詞のディクショナリ

    while node:
        # 単語をUnicodeに変換
        word = node.surface.decode("utf-8")
        words.append(word)

        # 品詞を取得
        pos=node.feature.split(',')[0]

        # 単語と品詞を格納
        if word not in pos_dict:
            pos_dict[word]=pos

        node=node.next

    parsed_words_dict={
        "all":words[1:-1], # 先頭と末尾は空文字のため除く
        "pos":pos_dict
    }
    return parsed_words_dict

# マルコフ連鎖が格納対象かどうか
def is_store_target(chain, pos_dict):
    for word in chain:
        if not word:
            return False

    # 先頭が名詞でなければ格納しない
    if pos_dict[chain[0]] !="名詞":
        return False
    # 末尾が名詞でなければ格納しない
    if pos_dict[chain[-1]] !="名詞":
        return False
    # 記号が含まれていたら格納しない
    for word in chain:
        #print pos_dict[word]
        if pos_dict[word] == "記号":
            return False
    return True

# マルコフ連鎖のリストとマルコフ連鎖の出現数を返す
# wordlist: 単語のリスト
# pos_dict: 単語と品詞のディクショナリ、品詞;"名詞","動詞"...
# chain_number: マルコフ連鎖の連鎖数
def get_markov_chain(wordlist, pos_dict, chain_number):
    markov={}
    count={}
    key=[]

    # マルコフ連鎖のキーを初期化
    for i in range(0, chain_number-1):
        key.append("")

    for word in wordlist:
        # キーをtupleからlistに変換、現在の単語を取得してマルコフ連鎖に追加
        chain=list(key)
        chain.append(word)

        if(is_store_target(chain,pos_dict)):
            # キーをlistからtupleに変換（listだとディクショナリのキーとして使えない）
            key_tuple = tuple(key)

            if key_tuple not in markov:
                markov[key_tuple]=[]
            markov[key_tuple].append(word)

            if (key_tuple,word) not in count:
                count[key_tuple,word]=0
            count[key_tuple,word]+=1

        # 次のマルコフ連鎖
        key.pop(0)
        key.append(word)

    return (markov,count)

# 標準出力
# markov: マルコフ連鎖のディクショナリ
# count: 単語と各文字列の出現回数のディクショナリ
def output(markov, count):
    for key in markov.keys():
        words=""

        # マルコフ連鎖の単語を連結する
        for word in key:
            words += word
        words += markov[key][0]

        # 2回以上出現したものを出力
        if count[key,markov[key][0]] > 1:
            print words, ' ', count[key,markov[key][0]]

if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 3):
        print "input filename and chain number."
        quit()

    filename = argvs[1]
    chain_number = int(argvs[2])

    src=open(filename, "r").read()
    words_dict=get_parsed_words_dict(src)

    # 分かち書き
    wordlist=words_dict['all']

    # 単語と品詞のディクショナリ
    pos_dict=words_dict['pos']

    markov = {}
    count = {}

    markov,count = get_markov_chain(wordlist,pos_dict,chain_number)
    output(markov,count)
