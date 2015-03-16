define("ember-bootstrap", ["ember-bootstrap/index","exports"], function(__index__, __exports__) {
  "use strict";
  Object.keys(__index__).forEach(function(key){
    __exports__[key] = __index__[key];
  });
});

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
define('ember-bootstrap/components/bs-button', ['exports', 'ember', 'ember-bootstrap/mixins/type-class', 'ember-bootstrap/mixins/size-class'], function (exports, Ember, TypeClass, SizeClass) {

   'use strict';

   exports['default'] = Ember['default'].Component.extend(TypeClass['default'], SizeClass['default'], {
       tagName: 'button',

       /**
        * @property classNames
        * @type array
        * @default ['btn']
        * @protected
        */
       classNames: ['btn'],

       /**
        * @property classNameBindings
        * @type array
        * @default ['active', 'block:btn-block']
        * @protected
        */
       classNameBindings: ['active', 'block:btn-block'],

       /**
        * @property classTypePrefix
        * @type String
        * @default 'btn'
        * @protected
        */
       classTypePrefix: 'btn',

       /**
        * @property attributeBindings
        * @type array
        * @default ['id', 'disabled', 'buttonType:type']
        * @protected
        */
       attributeBindings: ['id', 'disabled', 'buttonType:type'],

       /**
        * Default label of the button. Not need if used as a block component
        *
        * @property defaultText
        */
       defaultText: null,

       /**
        * Property to disable the button
        *
        * @property disabled
        */
       disabled: false,

       /**
        * Set the type of the button, either 'button' or 'submit'
        *
        * @property buttonType
        * @type String
        * @default 'button'
        */
       buttonType: 'button',

       /**
        * Set the 'active' class to apply active/pressed CSS styling
        *
        * @property active
        * @type boolean
        * @default false
        */
       active: false,

       /**
        * Property for block level buttons
        *
        * See the [Bootstrap docs](http://getbootstrap.com/css/#buttons-sizes)
        * @property block
        * @type boolean
        * @default false
        */
       block: false,

       /**
        * If toggle property is true, clicking the button will toggle the active state
        *
        * @property toggle
        * @type boolean
        * @default false
        */
       toggle: false,

       /**
        * If button is active and this is set, the icon property will match this property
        *
        * @property iconActive
        * @type String
        */
       iconActive: null,

       /**
        * If button is inactive and this is set, the icon property will match this property
        *
        * @property iconInactive
        * @type String
        */
       iconInactive: null,

       /**
        * Class(es) (e.g. glyphicons or font awesome) to use as a button icon
        * This will render a <i class="{{icon}}"></i> element in front of the button's label
        *
        * @property icon
        * @type String
        */
       icon: Ember['default'].computed('active', function() {
           if (this.get('active')) {
               return this.get('iconActive');
           } else {
               return this.get('iconInactive');
           }
       }),


       /**
        * Supply a value that will be associated with this button. This will be send
        * as a parameter of the default action triggered when clicking the button
        *
        * @property value
        * @type any
        */
       value: null,

       /**
        * State of the button. The button's label (if not used as a block component) will be set to the
        * `<state>Text` property.
        * This property will automatically be set when using a click action that supplies the callback with an promise
        *
        * @property textState
        * @type String
        * @default 'default'
        */
       textState: 'default',

       /**
        * Set this to true to reset the state. A typical use case is to bind this attribute with ember-data isDirty flag.
        *
        * @property reset
        * @type boolean
        */
       reset: null,

       /**
        * This will reset the state property to 'default', and with that the button's label to defaultText
        *
        * @method resetState
        */
       resetState: function() {
           this.set('textState', 'default');
       },

       resetObserver: Ember['default'].observer('reset', function(){
           if(this.get('reset')){
               this.resetState();
           }
       }),

       text: Ember['default'].computed('textState', 'defaultText', 'pendingText', 'resolvedText', 'rejectedText', function() {
           return this.getWithDefault(this.get('textState') + 'Text', this.get('defaultText'));
       }),

       /**
        * Click handler. This will send the default "action" action, with the following parameters:
        * * value of the button (that is the value of the "value" property)
        * * original event object of the click event
        * * callback: call that with a promise object, and the buttons state will automatically set to "pending", "resolved" and/or "rejected"
        *
        * @method click
        * @protected
        * @param evt
        */
       click: function(evt) {
           if (this.get('toggle')) {
               this.toggleProperty('active');
           }
           var that = this;
           var callback = function(promise) {
               if (promise) {
                   that.set('textState', 'pending');
                   promise.then(
                       function(){
                           if (!that.get('isDestroyed')) {
                               that.set('textState', 'resolved');
                           }
                       },
                       function(){
                           if (!that.get('isDestroyed')) {
                               that.set('textState', 'rejected');
                           }
                       }
                   );
               }
           };
           this.sendAction('action', this.get('value'), evt, callback);
       }


   });

});
define('ember-bootstrap/mixins/size-class', ['exports', 'ember'], function (exports, Ember) {

    'use strict';

    exports['default'] = Ember['default'].Mixin.create({
        classTypePrefix: Ember['default'].required(String),
        classNameBindings: ['sizeClass'],
        sizeClass: (function() {
            var prefix = this.get('classTypePrefix'),
                size = this.get('size');
            return Ember['default'].isBlank(size) ? null : prefix + '-' + size;
        }).property('size'),


        /**
         * Property for size styling, set to 'lg', 'sm' or 'xs'
         *
         * Also see the [Bootstrap docs](http://getbootstrap.com/css/#buttons-sizes)
         *
         * @property size
         * @type String
         */
        size: null
    });

});
define('ember-bootstrap/mixins/type-class', ['exports', 'ember'], function (exports, Ember) {

    'use strict';

    exports['default'] = Ember['default'].Mixin.create({
        classTypePrefix: Ember['default'].required(String),
        classNameBindings: ['typeClass'],
        typeClass: (function() {
            var prefix = this.get('classTypePrefix'),
                type = this.get('type') || 'default';
            return prefix + '-' + type;
        }).property('type'),


        /**
         * Property for type styling
         *
         * For the available types see the [Bootstrap docs](http://getbootstrap.com/css/#buttons-options) (use without "btn-" prefix)
         *
         * @property type
         * @type String
         * @default 'default'
         */
        type: 'default'
    });

});//# sourceMappingURL=addons.map