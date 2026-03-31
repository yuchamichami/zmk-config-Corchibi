# キーマップ描画：トラボやロータリーエンコーダを描く
[!NOTE]
  トラボやエンコーダの位置には[&trans]ではなく、ご面倒でもレイヤー毎にモジュールのbehaviorを設定してください。

## 1. 自分のCorchibiの[キーマップエディタ](https://nickcoutsos.github.io/keymap-editor/)を開いたら、トラボを置きたいキーを選択します。
![alt text](image1.png)

## 2. Behaviorを選択します。
![alt text](image2.png)

## 3. メニューから置きたいモジュール用のBehaviorを選びます。

| モジュール | 文字 | behavior |
| :--- | :--- | :--- |
| 19mmトラボ | Mouse | &TB1_mouse |
| 19mmトラボ | Scroll | &TB1_scroll |
| 14mmトラボ | Mouse | &TB2_mouse |
| 14mmトラボ | Scroll | &TB2_scroll |

![alt text](image3.png)

## 4. Saveしてコミットメッセージを入れてActionタブでワークフローが終わるのを待ちましょう
![alt text](image4.png)
![alt text](image5.png)

## 5. 終了するとトップページにREADME.mdが表示されるのでそこに反映されます。
![alt text](image6.png)
