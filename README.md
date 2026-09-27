# mossan-auth-common

Mossan Store 配下の各Flaskアプリで利用する共通認証パッケージです。

出欠ボード＋の運用中の認証フローを基準に、次を共通化します。

- ログイン、パスワード再設定の画面
- 認証画面のCSS
- 登録確認、パスワード再設定などのメール文面
- 認証ポリシーの既定値
- 認証関連DBの論理スキーマ

アカウントデータと業務データはアプリごとのDBへ保存します。このパッケージは、各アプリのDB接続や業務権限を管理しません。

## 基準値

- 登録確認URL: 24時間
- パスワード再設定URL: 1時間
- ログイン状態保持: 30日
- パスワード: 8文字以上（出欠ボード＋の現状値。今後見直し可能）

## Flaskアプリでの利用例

```python
from flask_wtf.csrf import generate_csrf

from mossan_auth_common.flask_ui import AuthUIConfig, init_auth_ui, render_login

init_auth_ui(
    app,
    AuthUIConfig(
        app_name="出欠ボード＋",
        logo_text="出欠ボード＋",
        logo_href="https://example.com/",
        login_url="/admin/login",
    ),
)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login_entry():
    # 認証処理はアプリ側で行う
    return render_login(
        csrf_token=generate_csrf(),
        form_action="/admin/login",
        forgot_password_url="/admin/password/forgot",
    )
```

上の例ではFlask-WTFを使用します。認証フォームを表示するアプリでは、Flask-WTFなどを
アプリ側の依存関係へ追加し、CSRFトークンを生成・検証してください。
共通テンプレートはCSRFトークンを必須としますが、POST時の検証はアプリ側の責任です。

認証ポリシーの値は共通の基準値です。ログイン試行回数、登録試行回数、URLの有効期限、
セッションCookie、パスワードハッシュ、権限確認は各アプリのサーバー側で必ず適用してください。

## 開発時の確認

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
```

実際の配布ではバージョンタグを固定し、テスト後に各アプリを順次更新します。最新版の無条件自動取得は行いません。

`0.2.1`では、認証画面の見た目を基準アプリである出欠ボード＋の従来デザインへ戻しました。
`0.2.0`と認証処理の呼び出し方法は同じで、DBや認証ロジックへの変更はありません。

`0.2.2`では、共通レイアウトを維持したままアプリ固有のロゴ字体と接尾文字の色を指定できます。
既定値は従来の手書き風ロゴであるため、`0.2.1`の利用アプリの表示は変わりません。

`0.2.3`では、管理者ログイン画面を縦一列のフォームへ整理し、任意の補助文を
`login_helper_message`で表示できます。認証、DB、セッション、CSRFの処理は変更していません。
補助文の既定値は空であるため、既存アプリの呼び出しとの後方互換性を維持します。

```python
AuthUIConfig(
    app_name="LightSketch+",
    logo_text="LightSketch+",
    logo_href="https://example.com/lightsketch/",
    login_url="/login",
    logo_variant="product",
    logo_main_text="LightSketch",
    logo_suffix_text="+",
    logo_accent_color="#ff8a00",
)
```
