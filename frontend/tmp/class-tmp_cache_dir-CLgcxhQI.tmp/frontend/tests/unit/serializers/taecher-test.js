define('frontend/tests/unit/serializers/taecher-test', ['ember-qunit'], function (ember_qunit) {

  'use strict';

  ember_qunit.moduleFor("serializer:taecher", {});

  // Replace this with your real tests.
  ember_qunit.test("it exists", function (assert) {
    var serializer = this.subject();
    assert.ok(serializer);
  });

  // Specify the other units that are required for this test.
  // needs: ['serializer:foo']

});