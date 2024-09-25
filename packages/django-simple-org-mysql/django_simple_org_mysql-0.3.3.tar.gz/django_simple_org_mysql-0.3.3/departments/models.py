from copy import deepcopy

from django.db import models


class MysqlArray(models.JSONField):
    def __init__(self, verbose_name=None, name=None, default=list, **kwargs):
        super().__init__(verbose_name, name, default=default, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后更新时间")

    class Meta:
        abstract = True


class Department(BaseModel):
    """
    部门表
    """

    name = models.CharField(max_length=32, verbose_name="部门名称")
    path = MysqlArray(null=True, verbose_name="所属部门路径")
    organization_id = models.IntegerField(verbose_name="组织id")
    charger_id = models.IntegerField(null=True, verbose_name="负责人ID")
    show_order = models.IntegerField(verbose_name="顺序", default=0)
    is_deleted = models.BooleanField(default=False, verbose_name="部门是否删除, 默认False")

    def get_children(self, department: dict):

        children = department.get("children")
        if not children:
            return
        for i in children:
            # 获取path
            path = deepcopy(i.get("path"))
            path.append(i.get("id"))
            path_str = ",".join([str(j) for j in path])
            # 查询是否有子节点
            child = self.child_map.get(path_str)
            if child:
                i["children"] = child
                # 存在子节点 继续递归调用
                self.get_children(i)
            else:
                i["children"] = []

    def department_tree(self):
        """
        获取树状结构
        @return:
        """
        child = Department.objects.filter(path__0=self.id, is_deleted=False)
        child_map = {}
        # 保存每个节点数据的 一级子节点
        for i in child:
            path_str = ",".join([str(j) for j in i.path])
            i_dict = {
                "id": i.id,
                "name": i.name,
                "charger_id": i.charger_id,
                "path_name": [Department.objects.get(pk=id_).name for id_ in i.path + [i.id]],
                "path": i.path,
                "show_order": i.show_order,
            }
            if path_str not in child_map:
                child_map[path_str] = [i_dict]
            else:
                tmp = child_map[path_str]
                tmp.append(i_dict)
                child_map[path_str] = tmp
        # 准备第一层数据
        res = {
            "id": self.id,
            "name": self.name,
            "charger_id": self.charger_id,
            "path_name": [self.name],
            "path": [],
            "show_order": self.show_order,
            "children": child_map.get(str(self.id), []),
        }
        self.child_map = child_map
        # 递归调用
        self.get_children(res)

        return res

    class Meta:
        db_table = "department"
        ordering = ["show_order"]
        indexes = [models.Index(fields=["organization_id", "is_deleted"])]
        # unique_together = [
        #     "name", "organization_id"
        # ]


class DepartmentUserMap(BaseModel):
    """
    部门和用户的关系映射表
    """

    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="部门id")
    user_id = models.IntegerField(verbose_name="用户id")

    class Meta:
        db_table = "department_user_map"
        unique_together = ["department", "user_id"]


class UserInformation(BaseModel):
    """
    用户信息表
    """

    user_id = models.IntegerField(verbose_name="用户id", unique=True)
    position = models.CharField(max_length=64, verbose_name="职位")
    leader_user_id = models.IntegerField(verbose_name="直属领导id")
    is_deleted = models.BooleanField(default=False, verbose_name="部门是否删除, 默认False")

    class Meta:
        db_table = "user_information"


class Role(BaseModel):
    """ "
    角色表
    """

    name = models.CharField(max_length=32, verbose_name="角色名称")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="角色描述")
    organization_id = models.IntegerField(verbose_name="组织id")
    is_deleted = models.BooleanField(default=False, verbose_name="是否被删除，默认没有被删除")
    is_enabled = models.BooleanField(default=True, verbose_name="是否被启用，默认被启用")
    is_edited = models.BooleanField(default=True, verbose_name="是否可以被删除，编辑")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "middle_roles"
        verbose_name = "角色"
        unique_together = ["name", "organization_id"]


class UserRole(BaseModel):
    """
    用户角色表
    """

    user_id = models.IntegerField(verbose_name="用户ID")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="角色")

    class Meta:
        db_table = "middle_user_roles_map"
        verbose_name = "用户角色关系表"
        unique_together = ["user_id", "role"]


class Position(BaseModel):
    """
    岗位表
    """

    name = models.CharField(max_length=32, verbose_name="岗位名称")
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name="岗位描述")
    organization_id = models.IntegerField(verbose_name="组织id")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除，默认不删除")
    is_edited = models.BooleanField(default=True, verbose_name="是否可以被删除，编辑")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "middle_position"
        verbose_name = "岗位"
        unique_together = ["name", "organization_id"]


class UserPosition(BaseModel):
    """
    岗位用户表
    """

    user_id = models.IntegerField(verbose_name="用户id")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="岗位")

    class Meta:
        db_table = "middle_user_position_map"
        verbose_name = "用户岗位关系表"
        unique_together = ["user_id", "position"]
