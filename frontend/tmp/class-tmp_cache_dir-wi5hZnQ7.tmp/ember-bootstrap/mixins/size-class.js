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