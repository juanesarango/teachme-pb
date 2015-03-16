export default Ember.HTMLBars.template((function() {
  var child0 = (function() {
    return {
      isHTMLBars: true,
      blockParams: 0,
      cachedFragment: null,
      hasRendered: false,
      build: function build(dom) {
        var el0 = dom.createDocumentFragment();
        var el1 = dom.createElement("i");
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode(" ");
        dom.appendChild(el0, el1);
        return el0;
      },
      render: function render(context, env, contextualElement) {
        var dom = env.dom;
        var hooks = env.hooks, element = hooks.element;
        dom.detectNamespace(contextualElement);
        var fragment;
        if (env.useFragmentCache && dom.canClone) {
          if (this.cachedFragment === null) {
            fragment = this.build(dom);
            if (this.hasRendered) {
              this.cachedFragment = fragment;
            } else {
              this.hasRendered = true;
            }
          }
          if (this.cachedFragment) {
            fragment = dom.cloneNode(this.cachedFragment, true);
          }
        } else {
          fragment = this.build(dom);
        }
        var element0 = dom.childAt(fragment, [0]);
        element(env, element0, context, "bind-attr", [], {"class": "icon"});
        return fragment;
      }
    };
  }());
  return {
    isHTMLBars: true,
    blockParams: 0,
    cachedFragment: null,
    hasRendered: false,
    build: function build(dom) {
      var el0 = dom.createDocumentFragment();
      var el1 = dom.createTextNode("");
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("");
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("");
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("");
      dom.appendChild(el0, el1);
      return el0;
    },
    render: function render(context, env, contextualElement) {
      var dom = env.dom;
      var hooks = env.hooks, get = hooks.get, block = hooks.block, content = hooks.content;
      dom.detectNamespace(contextualElement);
      var fragment;
      if (env.useFragmentCache && dom.canClone) {
        if (this.cachedFragment === null) {
          fragment = this.build(dom);
          if (this.hasRendered) {
            this.cachedFragment = fragment;
          } else {
            this.hasRendered = true;
          }
        }
        if (this.cachedFragment) {
          fragment = dom.cloneNode(this.cachedFragment, true);
        }
      } else {
        fragment = this.build(dom);
      }
      if (this.cachedFragment) { dom.repairClonedNode(fragment,[0,1,2,3]); }
      var morph0 = dom.createMorphAt(fragment,0,1,contextualElement);
      var morph1 = dom.createMorphAt(fragment,1,2,contextualElement);
      var morph2 = dom.createMorphAt(fragment,2,3,contextualElement);
      block(env, morph0, context, "if", [get(env, context, "icon")], {}, child0, null);
      content(env, morph1, context, "text");
      content(env, morph2, context, "yield");
      return fragment;
    }
  };
}()));