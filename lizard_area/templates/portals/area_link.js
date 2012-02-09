{% load get_grid %}
{% load get_portal_template %}

{% if perms.auth.is_analyst %}

{
    itemId: 'gebiedslink-beheer',
    title: 'gebiedenlink',
	xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'gebiedenlink-beheer'
        }
    ],
	items:[{
		flex:1,
		items: [{
            title: 'Gebiedenlink',
            anchor:'100%',
            flex:1,
            xtype: 'leditgrid',
            columnLines: true,
            plugins: [
                'applycontext'
            ],
            applyParams: function(params) {
                var params = params|| {};
                console.log('apply params');
                console.log(params);

                if (this.store) {
                    //this.store.applyParams({object_id: params.object_id,
                    //                        area_object_type: 'Structure'});
                    this.store.load();
                }
            },
            //proxyUrl: '/portal/wbstructures.json',
            proxyUrl: '/area/api/area_link/',
            proxyParams: {
                flat: false
            },
            dataConfig:[
                //is_computed altijd 1 in en 1 uit en verder niet
                {name: 'id', title: 'id', editable: false, visible: false, width: 30, type: 'number'},
                {name: 'area_a', title: 'krw-gebied', editable: true, visible: true, width: 300,
                    type: 'combo', remote: true, store: {
                        fields: ['id', 'name'],
                        proxy: {
                            type: 'ajax',
                            url: '/area/api/krw-areas/?node=root&_accept=application%2Fjson&size=id_name',
                            reader: {
                                type: 'json',
                                root: 'areas'
                            }
                        }
                    }
                },
                {name: 'area_b', title: 'aan-afvoergebied', editable: true, visible: true, width: 300,
                    type: 'combo', remote: true, store: {
                        fields: ['id', 'name'],
                        proxy: {
                            type: 'ajax',
                            url: '/area/api/catchment-areas/?_accept=application%2Fjson&size=id_name',
                            reader: {
                                type: 'json',
                                root: 'areas'
                            }
                        }
                    }
                }
           ]
        }]
	}]
}
{% else %}
    {% get_portal_template geen_toegang %}
{% endif %}
