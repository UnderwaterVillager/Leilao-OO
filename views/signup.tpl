<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="/static/styles/userpage.css">
</head>
<body>
    <form method="POST" action="/signup">
        <label for="username">Nome de Usuário:</label>
        <input id="username" name="username" type="text">
        
        <label for="email">Email:</label>
        <input id="email" name="email" type="text">
        
        <label for="password">Senha</label>
        <input id="password" name="password" type="text">
        
        <input type="submit">
    </form>
    <div>
        % if error:
            <p>{{error}}</p>
        % end
    </div>
    <script src="/static/scripts/signup.js"></script>
</body>
</html>