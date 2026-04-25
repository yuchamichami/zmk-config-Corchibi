# 自分用のキーマップ画像を描く

トップページ(README.md)のキーマップ画像は[Keymap-drawer](https://github.com/caksoylar/keymap-drawer)を使っています。<br>
[キーマップエディタ](https://nickcoutsos.github.io/keymap-editor/)で編集してSaveすることで、GitHubのワークフローによって自動的に更新されます。<br>

> [!NOTE]
>キーマップ直編集の方はコミットすればOK<br>
>カラーテーマ（※後述）に問題が無ければ、描画のためにすることは何もありません。

---

## 1. カラーテーマを変更する（初回のみ）

キーボード本体の色に合わせたカラーテーマを選んでキーマップ画像を生成できます。

> [!NOTE]
> この設定は初回のみ必要な作業です。 （もちろん後で変更も可能）<br>
> ご自分専用のテーマも設定可能なので、手順を公開する予定です。

### 利用可能なプリセット

| テーマ名 | サンプル |
| :--- | ---: |
| `black` | ![black theme sample](theme_black.png) |
| `white` | ![white theme sample](theme_white.png) |

### テーマの設定方法

リポジトリ内の `keymap-drawer/theme.txt` を開き、使いたいテーマ名に書き換えてコミットします。

```
black
```

または

```
white
```

> [!NOTE]
> テーマを変更するとき以外は、このファイルを触る必要はありません。

#### お試しでテーマを一時的に変えたいとき

コミットせずに別テーマを試してみることが可能です。<br>
GitHubの **Actionsタブ** から以下の手順で実行できます。

1. リポジトリの **Actions** タブを開く
2. 左のワークフロー一覧から **Draw Keymap** を選択
3. **Run workflow** ボタンをクリック
4. ドロップダウンからテーマ名を選んで **Run workflow** を実行

> [!NOTE]
> この方法はその1回の描画にのみ適用されます。<br>
（`theme.txt` の内容は変更されません。）


---

## 2. トラボを描画したい

今のところCorchibiのトラボ位置をキーマップ画像に自動反映することはできませんが、<br>
KeymapEditor上で専用behaviorを選択していただことで描画することが可能です。

> [!NOTE]
> お手数ですがデフォルトだけでなく、全てのレイヤーで専用behaviorを設定してください。
>`[&trans]`ではトラボ画像になりません。



### (1). キーマップエディタを開く

自分のCorchibiの[キーマップエディタ](https://nickcoutsos.github.io/keymap-editor/)を開いたら、トラボを置きたいキーを選択します。
![alt text](image1.png)

### (2). Behaviorを選択します。
![alt text](image2.png)

### (3). メニューから置きたいモジュール用のBehaviorを選びます。

| モジュール | 文字 | behavior |
| :--- | :--- | :--- |
| 19mmトラボ | Mouse | &TB1_mouse |
| 19mmトラボ | Scroll | &TB1_scroll |
| 14mmトラボ | Mouse | &TB2_mouse |
| 14mmトラボ | Scroll | &TB2_scroll |

![alt text](image3.png)

### (4). Saveしてコミットメッセージを入れてActionタブでワークフローが終わるのを待ちましょう
![alt text](image4.png)
![alt text](image5.png)

### (5). 終了するとトップページにREADME.mdが表示されるのでそこに反映されます。
![alt text](image6.png)
