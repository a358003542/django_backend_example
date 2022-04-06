import connexion
import six

from swagger_server import util


def api_accept_invite_partial_update(company_name):  # noqa: E501
    """api_accept_invite_partial_update

    用户接受某个公司的邀请 # noqa: E501

    :param company_name: 
    :type company_name: str

    :rtype: None
    """
    return 'do some magic!'


def api_self_get_company():  # noqa: E501
    """api_self_get_company

    获取用户当前所在的公司的公司信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'

def api_new_company():  # noqa: E501
    """api_new_company

    获取用户当前所在的公司的公司信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'

def api_change_company():  # noqa: E501
    """api_change_company

    获取用户当前所在的公司的公司信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'

def api_company_read(company_name):  # noqa: E501
    """api_company_read

    获取公司信息 # noqa: E501

    :param company_name: 
    :type company_name: str

    :rtype: None
    """
    return 'do some magic!'


def api_department_create():  # noqa: E501
    """增加部门

    请求格式 {&#39;department&#39;: {&#39;name&#39;: ...}} # noqa: E501


    :rtype: None
    """
    return 'do some magic!'



def api_invite_partial_update(username):  # noqa: E501
    """邀请某个用户加入公司

    # 需要本用户有 can_invite_people 权限 # noqa: E501

    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_organization_list():  # noqa: E501
    """api_organization_list

    查看自己的组织信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_organization_partial_update(username):  # noqa: E501
    """修改其他用户的组织信息

    相同公司 需要有Organization模型的change权限 # noqa: E501

    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_organization_read(username):  # noqa: E501
    """查看其他用户的组织信息

    只有本公司内才能查看 # noqa: E501

    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_organization_roles_add_create(role_name, username):  # noqa: E501
    """api_organization_roles_add_create

    将用户添加进某个角色 # noqa: E501

    :param role_name: 
    :type role_name: str
    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_organization_roles_remove_create(role_name, username):  # noqa: E501
    """api_organization_roles_remove_create

    将用户移除出某个角色 # noqa: E501

    :param role_name: 
    :type role_name: str
    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_profiles_read(username):  # noqa: E501
    """查看其他用户的档案信息

    暂定为相同的公司都可以彼此查看彼此的档案信息 # noqa: E501

    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def api_role_add_permission_create(role_id):  # noqa: E501
    """角色增加权限

    {     &#39;model&#39;: &#39;app_label.model_name&#39; } # noqa: E501

    :param role_id: 
    :type role_id: str

    :rtype: None
    """
    return 'do some magic!'


def api_role_create():  # noqa: E501
    """api_role_create

    增加一个新的角色 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_role_remove_permission_create(role_id):  # noqa: E501
    """api_role_remove_permission_create

     # noqa: E501

    :param role_id: 
    :type role_id: str

    :rtype: None
    """
    return 'do some magic!'


def api_upload_file_update(filename):  # noqa: E501
    """api_upload_file_update

    wb+ put 文件新建或者替换模式 # noqa: E501

    :param filename: 
    :type filename: str

    :rtype: None
    """
    return 'do some magic!'


def api_upload_image_update(filename):  # noqa: E501
    """api_upload_image_update

     # noqa: E501

    :param filename: 
    :type filename: str

    :rtype: None
    """
    return 'do some magic!'


def api_user_list():  # noqa: E501
    """用户获取自己的一些信息

    也包括自己的档案信息和组织信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_user_login_create():  # noqa: E501
    """用户登录

    用户登录单独编写，基本上任何人都可以访问。 登录 用户名或邮箱都可 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_user_partial_update():  # noqa: E501
    """用户修改自己的信息

    不能修改自己的组织信息 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_user_phone_login_create():  # noqa: E501
    """手机登录附带自动注册过程

    {     &#39;user&#39;:{         &#39;phone&#39;:         &#39;biz_id&#39;:         &#39;verification_code&#39;:         &#39;send_date&#39;     } } # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def api_user_registration_create():  # noqa: E501
    """用户注册需要提供用户名+邮箱+密码

    注册接口单独写，基本上任何人都可以注册。 # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
