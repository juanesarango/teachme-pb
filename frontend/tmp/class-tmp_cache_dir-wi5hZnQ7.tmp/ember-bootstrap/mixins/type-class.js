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

});