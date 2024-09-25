# -*- coding: utf-8 -*-
"""
@File        : request_test.py
@Author      : yu wen yang
@Time        : 2022/5/10 1:23 下午
@Description :
"""
import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_simple_departments.settings')
django.setup()
if __name__ == '__main__':
    from departments.views.roles import RoleControl
    from departments.views.department import create_department, DepartmentControl
    from departments.views.position import PositionViewSet

    # def response(func):
    #     def wrapper(*args, **kwargs):
    #         res = func(*args, **kwargs)
    #         print(json.loads(res.content))
    #     return wrapper
    #
    # # 创建部门
    # @response
    # def create_department_():
    #     post_data = {
    #         "name": "python",
    #         "parent_id": 2,
    #         "charger_id": None,
    #         "organization_id": 1
    #     }
    #     res = create_department(post_data)
    #     return res

    obj = DepartmentControl(1)
    # print(obj.root)

    # print(obj.list("sub", 2))
    # print(obj.list("all"))
    # print(obj.list("all", department_name="o"))
    # print(obj.create({"name": "前端o99", "parent_id": 2}))
    # print(obj.retrieve(3))
    # print(obj.update(18, {"name": "前端91", "parent_id": None, "charger_id": None}))
    # print(obj.update(18, {"name": "前端91", "parent_id": None, "charger_id": None}))
    # print(obj.update_root(1, {"name": "八分量"}))
    # print(obj.delete(2))
    # print(obj.move_show_order({"department_id": 4, "type": "up"}))
    # print(obj.create_department_user(5, [1, 2, 3]))
    # print(obj.department_user_list([6]))
    # print(obj.delete_department_user(5, [11]))
    # print(obj.get_chargers())
    # print(obj.organization_user_list())
    # print(obj.exclude(5))
    # print(obj.change(1, []))
    # print(obj.user_departments(1))

    # obj = RoleViewSet(1)
    # print(obj.create({"name": "xx"}))
    # print(obj.list())
    # print(obj.list("角色"))
    # print(obj.retrieve(5))
    # print(obj.update(3, {"name": "第二个角色", "desc": 123}))
    # print(obj.delete(6))
    # print(obj.edit(7))
    # print(obj.edit(7))
    # print(obj.create_role_user(3, [1, 2, 3]))
    # print(obj.role_user_list(1))
    # print(obj.change(1, [1, 2, 3]))
    # print(obj.delete_role_user(1, [1, 2, 3]))

    # obj = PositionViewSet(1)
    # print(obj.create({"name": "岗位1", "desc": ""}))
    # print(obj.list())
    # print(obj.list("这是"))
    # print(obj.retrieve(1))
    # print(obj.update(1, {"name": "这是岗位1", "desc": "岗位1的描述"}))
    # print(obj.delete(3))
    # print(obj.create_position_user(1, [5, 6, 7]))
    # print(obj.change(1, [1,]))
    # print(obj.position_user_list(1))
    # print(obj.delete_position_user(2, [1, 2, 3]))




