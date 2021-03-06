#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def action_link(action, cgihome):
    from ActionLinkRenderer import ActionLinkRenderer
    renderer = ActionLinkRenderer( cgihome )
    return renderer.render( action )[0]

def action_href(action, cgihome):
    from ActionHrefRenderer import ActionHrefRenderer
    renderer = ActionHrefRenderer( cgihome )
    return renderer.render( action )

def action_formfields( action, form ):
    from ActionMill_forForm import ActionMill_forForm
    renderer = ActionMill_forForm( form )
    return renderer.render( action )


def pageMill(configurations):
    from PageMill import PageMill
    return PageMill(configurations)


# version
__id__ = "$Id$"
__date__ = "$Jul 19, 2009 9:53:31 PM$"


