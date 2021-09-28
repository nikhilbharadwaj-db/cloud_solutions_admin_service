from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from config import *
from utils import *

app = Flask(__name__)
app.config.update(app_config_dict)
CORS(app)

db = SQLAlchemy(app)
db.init_app(app)

from models.Role import Role as RoleModel
from models.Entity import Entity as EntityModel
from models.User import User as UserModel
from models.UserRoleMapping import UserRoleMapping as UserRoleMappingModel

from routes import User

with app.app_context():
    db.create_all()

role_names: [str] = ['SUPERADMIN', 'ADMIN', 'USER']
print('Adding Roles')
try:
    roles = [RoleModel(role_name=role_name) for role_name in role_names]
    db.session.bulk_save_objects(roles)
    db.session.commit()
except:
    pass
print('Roles Added')

print('Adding Super Admin')
try:
    super_admin_password_enc = encrypt(secret_key=secret_key, plain_text=super_admin_password)
    super_admin_user = UserModel(user_name='super_admin', user_email='super_admin@nodomain.com',
                            password=super_admin_password_enc, first_name='Super Admin', last_name='User')
    db.session.add(super_admin_user)
    db.session.commit()

    super_admin_role: RoleModel = RoleModel.get_role_by_name(role_name=role_names[0])
    super_admin_user_role_mapping = UserRoleMappingModel(user_name=super_admin_user.user_name,
                                                    role_id=super_admin_role.role_id)
    db.session.add(super_admin_user_role_mapping)
    db.session.commit()
except Exception as e:
    pass
print('Super Admin Added')


@app.route('/')
def ping():  # put application's code here
    return 'pong'


if __name__ == '__main__':
    app.run()
