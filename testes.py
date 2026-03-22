from app import app, db
from app.models import User, Task

# with app.app_context():
#     database.create_all()


""" with app.app_context():
    usuario = User(
        name = 'Gabriel Seixas',
        email = 'gcseixas01@gmail.com',
        password = '123456',
        role = 'parent',
        parent_id = ''
    )
    db.session.add(usuario)
    db.session.commit() """

with app.app_context():
    meus_usuarios = User.query.all()
    for usuario in meus_usuarios:
        print(usuario.id, usuario.name, usuario.email, usuario.password, usuario.role, usuario.parent_id)




""" with app.app_context():
    minhas_tarefas = Task.query.all()
    for tarefa in minhas_tarefas:
        print(tarefa.title) """