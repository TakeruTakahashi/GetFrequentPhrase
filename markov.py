#!usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import random
import MeCab

def wakati(input_text):
    t=MeCab.Tagger("-Owakati")
    tagger=MeCab.Tagger("mecabrc")
    text=input_text.encode("utf-8")
    node=tagger.parseToNode(text)

    words=[]
    nouns=[]
    verbs=[]
    adjs=[]
    words=[]

    pos_dict={}

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


if __name__ == "__main__":
    filename = "/Users/tkrtkhsh/python/patent.txt"
    src=open(filename, "r").read()
    words_dict=wakati(src)

    # 分かち書き
    wordlist=words_dict['all']

    # 単語と品詞のdictionary
    pos_dict=words_dict['pos']

    # 連鎖数3のマルコフテーブルを生成
    markov ={}
    count={}
    w1=""
    w2=""
    for word in wordlist:
        if w1 and w2  and pos_dict[w1]=="名詞": # 先頭が名詞のもののみ格納
            if(w1,w2) not in markov:
                markov[(w1,w2)] = []

            # 出現回数を記録
            if(w1,w2,word) not in count:
                count[(w1,w2,word)]=0
            count[(w1,w2,word)]+=1

            markov[(w1,w2)].append(word)
        w1, w2 = w2, word

    # テーブル出力
    for key in markov.keys():
        # 2回以上出現したものを出力
        if count[key[0],key[1],markov[key][0]] > 1:
            print key[0],key[1], markov[key][0], ' ', count[key[0],key[1],markov[key][0]]
