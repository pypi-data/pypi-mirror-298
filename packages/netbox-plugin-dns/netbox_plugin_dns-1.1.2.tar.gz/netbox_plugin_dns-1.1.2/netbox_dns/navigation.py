from netbox.plugins import PluginMenuButton, PluginMenuItem, PluginMenu
from netbox.plugins.utils import get_plugin_config

menu_name = get_plugin_config("netbox_dns", "menu_name")
top_level_menu = get_plugin_config("netbox_dns", "top_level_menu")

view_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:view_list",
    link_text="Views",
    permissions=["netbox_dns.view_view"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:view_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_view"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:view_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_view"],
        ),
    ),
)

zone_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:zone_list",
    link_text="Zones",
    permissions=["netbox_dns.view_zone"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:zone_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_zone"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:zone_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_zone"],
        ),
    ),
)

nameserver_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:nameserver_list",
    link_text="Nameservers",
    permissions=["netbox_dns.view_nameserver"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:nameserver_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_nameserver"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:nameserver_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_nameserver"],
        ),
    ),
)

record_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:record_list",
    link_text="Records",
    permissions=["netbox_dns.view_record"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:record_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_record"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:record_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_record"],
        ),
    ),
)

managed_record_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:managed_record_list",
    link_text="Managed Records",
    permissions=["netbox_dns.view_record"],
)

zonetemplate_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:zonetemplate_list",
    link_text="Zone Templates",
    permissions=["netbox_dns.view_zonetemplate"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:zonetemplate_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_zonetemplate"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:zonetemplate_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_zonetemplate"],
        ),
    ),
)

recordtemplate_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:recordtemplate_list",
    link_text="Record Templates",
    permissions=["netbox_dns.view_recordtemplate"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:recordtemplate_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_recordtemplate"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:recordtemplate_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_recordtemplate"],
        ),
    ),
)

registrar_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:registrar_list",
    link_text="Registrars",
    permissions=["netbox_dns.view_registrar"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:registrar_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_registrar"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:registrar_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_registrar"],
        ),
    ),
)

contact_menu_item = PluginMenuItem(
    link="plugins:netbox_dns:registrationcontact_list",
    link_text="Registration Contacts",
    permissions=["netbox_dns.view_registrationcontact"],
    buttons=(
        PluginMenuButton(
            "plugins:netbox_dns:registrationcontact_add",
            "Add",
            "mdi mdi-plus-thick",
            permissions=["netbox_dns.add_registrationcontact"],
        ),
        PluginMenuButton(
            "plugins:netbox_dns:registrationcontact_import",
            "Import",
            "mdi mdi-upload",
            permissions=["netbox_dns.add_registrationcontact"],
        ),
    ),
)


if top_level_menu:
    menu = PluginMenu(
        label=menu_name,
        groups=(
            (
                "DNS Configuration",
                (
                    view_menu_item,
                    zone_menu_item,
                    nameserver_menu_item,
                    record_menu_item,
                    managed_record_menu_item,
                ),
            ),
            (
                "Templates",
                (
                    zonetemplate_menu_item,
                    recordtemplate_menu_item,
                ),
            ),
            (
                "Domain Registration",
                (
                    registrar_menu_item,
                    contact_menu_item,
                ),
            ),
        ),
        icon_class="mdi mdi-dns",
    )
else:
    menu_items = (
        view_menu_item,
        zone_menu_item,
        nameserver_menu_item,
        record_menu_item,
        managed_record_menu_item,
        registrar_menu_item,
        contact_menu_item,
    )
