define('ember-bootstrap/components/bs-button-group', ['exports', 'ember', 'ember-bootstrap/components/bs-button', 'ember-bootstrap/mixins/size-class'], function (exports, Ember, Button, SizeClass) {

    'use strict';

    exports['default'] = Ember['default'].Component.extend(SizeClass['default'], {

        /**
         * @type string
         * @property ariaRole
         * @default 'group'
         * @protected
         */
        ariaRole: 'group',

        /**
         * @property classNames
         * @type array
         * @default ['btn-group']
         * @protected
         */
        classNames: ['btn-group'],

        /**
         * @property classNameBindings
         * @type array
         * @protected
         */
        classNameBindings: ['vertical:btn-group-vertical','justified:btn-group-justified'],

        /**
         * @property classTypePrefix
         * @type String
         * @default 'btn-group'
         * @protected
         */
        classTypePrefix: 'btn-group',

        /**
         * Set to true for a vertically stacked button group, see http://getbootstrap.com/components/#btn-groups-vertical
         *
         * @property vertical
         * @type boolean
         * @default false
         * @public
         */
        vertical: false,

        /**
         * Set to true for the buttons to stretch at equal sizes to span the entire width of its parent.
         *
         * *Important*: You have to wrap every button component in a `div class="btn-group">`:
         *
         * ```handlebars
         * <div class="btn-group" role="group">
         * \{{#bs-button}}My Button{{/bs-button}}
         * </div>
         * ```
         *
         * See http://getbootstrap.com/components/#btn-groups-justified
         *
         * @property justified
         * @type boolean
         * @default false
         * @public
         */
        justified: false,

        /**
         * The type of the button group specifies how child buttons behave and how the `value` property will be computed:
         *
         * ### null
         * If `type` is not set (null), the button group will add no functionality besides Bootstrap styling
         *
         * ### radio
         * if `type` is set to "radio", the buttons will behave like radio buttons:
         * * the buttons will toggle (`toggle` property of the child buttons will be set to true)
         * * only one button may be active
         * * the `value` property of the button group will reflect the `value` property of the active button
         *
         * ### checkbox
         * if `type` is set to "checkbox", the buttons will behave like checkboxes:
         * * the buttons will toggle (`toggle` property of the child buttons will be set to true)
         * * any number of buttons may be active
         * * the `value` property of the button group will be an array containing the `value` properties of all active buttons
         *
         * @property type
         * @type string
         * @default null
         * @public
         */
        type: null,


        /**
         * The value of the button group, computed by its child buttons.
         * See the {{#crossLink "Button-Group/type:attribute"}}`type` property{{/crossLink}} for how the value property is constructed.
         *
         * When you set the value, the corresponding buttons will be activated:
         * * use a single value for a radio button group to activate the button with the same value
         * * use an aray of values for a checkbox button group to activate all the buttons with values contained in the array
         *
         * @property value
         * @type array|any
         * @public
         */
        value: Ember['default'].computed('activeChildren.@each.value','type',function(key, value){
            if (arguments.length>1) {
                var values = !Ember['default'].isArray(value) ? [value] : value;
                this.get('childButtons')
                    .forEach(function(button) {
                        button.set('active', values.contains(button.get('value')));
                    });
                return value;
            }
            switch (this.get('type')) {
                case 'radio':
                    return this.get('activeChildren.firstObject.value');
                case 'checkbox':
                    return this.get('activeChildren').mapBy('value');
            }
            return 1;
        }),

        /**
         * Array of all child buttons (instances of Bootstrap.Button)
         * @property childButtons
         * @type array
         * @protected
         */
        childButtons: Ember['default'].computed.filter('childViews', function(view) {
            return view instanceof Button['default'];
        }),


        /**
         * Child buttons that are active (pressed)
         * @property activeChildren
         * @type array
         * @protected
         */
        activeChildren: Ember['default'].computed.filterBy('childButtons', 'active', true),


        lastActiveChildren: [],
        newActiveChildren: Ember['default'].computed.setDiff('activeChildren','lastActiveChildren'),
        _observeButtons: Ember['default'].observer('activeChildren.[]','type', function() {
            if (this.get('type') !== 'radio') {
                return;
            }

            Ember['default'].run.scheduleOnce('actions',this, function(){
                // the button that just became active
                var newActive = this.get('newActiveChildren.firstObject');

                if (newActive) {
                    this.beginPropertyChanges();
                    this.get('childButtons').forEach(function(button){
                        if (button !== newActive) {
                            button.set('active', false);
                        }
                    });

                    this.endPropertyChanges();
                }
                // remember activeChildren, used as a replacement for a before observer as they will be deprecated in the future...
                this.set('lastActiveChildren', this.get('activeChildren').slice());
            });
        }),

        _observeType: Ember['default'].observer('type','childButtons.[]', function() {
            if (this.get('type') === 'radio' || this.get('type') === 'checkbox') {
                // set all child buttons to toggle
                this.get('childButtons').forEach(function(button) {
                    button.set('toggle', true);
                });
            }
        }),

        init: function() {
            this._super();
            this.get('activeChildren');
        }




    });

});