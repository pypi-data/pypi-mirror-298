from flask import render_template
from flask_login import current_user

def getMenu():
    return current_user.permissions.get("menu") if current_user and current_user.permissions and current_user.permissions.get("menu") else []

class MenuBase:
    title = "Menu"
    menu_opts = getMenu()

    @classmethod
    def renderFromFactory(cls, main_title, comps_data):        
        return cls.render(
            "macros/template_factory.html",
            main_title=main_title,
            comps_data=comps_data)

    @classmethod
    def render(cls, template_name_or_list: str| list[str], **context):        
        menu_data = {
            "title": cls.title,
            "opts": getMenu(),
        }
        return render_template(template_name_or_list, menu_data=menu_data, **context)
