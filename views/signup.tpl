<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="/signup" method="POST">
        Nome de Usuário:<input name="username" type="text">
        Email:<input name="email" type="text">
        Senha:<input name="password" type="text">
        Confirmar:<input type="submit">
    </form>
    % if error_message:
        <div>
            {error_message}
        </div>
    % end
</body>
</html>