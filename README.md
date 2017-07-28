# じゃんけん LINE chatbot

## 概要

チャットボットとは，「『チャット』と『ボット』を組み合わせた言葉で、人工知能を活用した『自動会話プログラム』（ITトレンド様から引用）」のことを指します．

2016年にLINEやFacebook Messenger など複数のSNSサービスが，chatbot のためのAPIを開放したため，いま大きな注目を集めています．
LINEやFacebook Messengerが抱える世界中のユーザーに対して，新規アプリをダウンロードすることなく，慣れ親しんだUIでアクセスできるため，ソフトウェア的な面白さだけでなく，ビジネス利用の展開も強く期待されています．

このプロジェクトは，LINE chatbot を活用したシステムのサンプルとして，LINE 上でじゃんけんができる仕組みを提供しています．
チャットボットへのアクセスは，以下のQRコードをLINEから読み込むだけで完了します．

![qr](https://user-images.githubusercontent.com/11922286/28660450-e657f046-72ed-11e7-929c-6e43c6ebdd40.png)

## 遊び方

このチャットボットは以下の4つの入力を受け付けます．
チャットボット上でどれかを入力すると対応する処理が実行されます．

* 「ぐー」: じゃんけんで「グー」を出します
* 「ぱー」: じゃんけんで「パー」を出します
* 「ちょき」: じゃんけんで「チョき」を出します
* 上記以外の任意のテキスト : これまでの累計勝利回数を提示します

実際に遊んでみたときの画面は以下の通りです．

![photo](https://user-images.githubusercontent.com/11922286/28700356-3d4f2242-738a-11e7-8077-7eabfd2a4dc7.jpg)


## LINE chatbot についてもっと知りたい方へ

### Colorfultalk Inc. チャットボット開発資料

#### キーワード : python, line_bot_sdk, flask, database, PaaS, heroku

LINE での chatbot 開発を進めていく上で必要となる知識についての資料をまとめています．
line_bot_sdkを利用して開発したボットを heroku 上で運用するまでを解説しています．
URL : https://github.com/colorfultalk/DevDoc

### LINE developers Messaging API 公式ドキュメント

LINE chatbot の開発は，LINE株式会社が公開している Messaging APIを利用します．
chatbot の開発時にはここを逐次参照しています．

URL : https://developers.line.me/messaging-api/overview

## お問い合わせ
提供している資料に関して，またチャットボットを用いたサービス開発についてのご相談は ikutani@colorfultalk.co.jp までお寄せください．

Copyright 2017 Colorfultalk inc. All Rights Reserved.