define('frontend/tests/unit/components/edit-textarea-test', ['ember-qunit'], function (ember_qunit) {

  'use strict';

  ember_qunit.moduleForComponent("edit-textarea", {});

  ember_qunit.test("it renders", function (assert) {
    assert.expect(2);

    // creates the component instance
    var component = this.subject();
    assert.equal(component._state, "preRender");

    // renders the component to the page
    this.render();
    assert.equal(component._state, "inDOM");
  });

  // specify the other units that are required for this test
  // needs: ['component:foo', 'helper:bar']

});