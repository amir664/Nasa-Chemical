/** @odoo-module **/

import {ActionMenus} from "@web/search/action_menus/action_menus";
import { registry } from "@web/core/registry";
import core from 'web.core';
var _t = core._t;
let registryActionId = 0;

ActionMenus.prototype.setActionItems = async function(props){
    // ************************************
    // Get restricted actions 
    const RestActions = await this.orm.call("access.management", "get_remove_options", [1,this.props.resModel]);
    // ************************************

    // Callback based actions
    let callbackActions = (props.items.other || []).map((action) =>
        Object.assign({ key: `action-${action.description}` }, action)
    );
    
    // Action based actions
    const actionActions = props.items.action || [];
    const formattedActions = actionActions.map((action) => ({
        action,
        description: action.name,
        key: action.id,
    }));
    // ActionMenus action registry components
    const registryActions = [];
    for (const { Component, getProps } of registry.category("action_menus").getAll()) {
        const itemProps = await getProps(props, this.env);
        if (itemProps) {
            registryActions.push({
                Component,
                key: `registry-action-${registryActionId++}`,
                props: itemProps,
            });
        }
    }
    // filter restricted callback actions
    if(RestActions.length){
        callbackActions = _.filter(callbackActions,function(val){
            return !_.contains(RestActions,val.description)
        })
    }
    return [...callbackActions, ...formattedActions, ...registryActions];
}