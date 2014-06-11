# -*- coding: utf-8 -*-
"""
===
sdc
===

Student demo cup registration
"""

#
# Register blueprint on app
#
def register_plugin(app):
    from .views import sdc

    app.register_blueprint(sdc)

    #from .admin import register_plugin

    #register_plugin(app)
