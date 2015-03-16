export default Ember.HTMLBars.template((function() {
  var child0 = (function() {
    return {
      isHTMLBars: true,
      blockParams: 0,
      cachedFragment: null,
      hasRendered: false,
      build: function build(dom) {
        var el0 = dom.createDocumentFragment();
        var el1 = dom.createTextNode("					");
        dom.appendChild(el0, el1);
        var el1 = dom.createElement("li");
        var el2 = dom.createElement("a");
        dom.setAttribute(el2,"href","/comparte");
        var el3 = dom.createTextNode("Enseña");
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode("\n");
        dom.appendChild(el0, el1);
        return el0;
      },
      render: function render(context, env, contextualElement) {
        var dom = env.dom;
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
        return fragment;
      }
    };
  }());
  var child1 = (function() {
    return {
      isHTMLBars: true,
      blockParams: 0,
      cachedFragment: null,
      hasRendered: false,
      build: function build(dom) {
        var el0 = dom.createDocumentFragment();
        var el1 = dom.createTextNode("					");
        dom.appendChild(el0, el1);
        var el1 = dom.createElement("li");
        var el2 = dom.createElement("a");
        dom.setAttribute(el2,"href","/teachouts");
        var el3 = dom.createTextNode("Sesiones");
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode("\n");
        dom.appendChild(el0, el1);
        return el0;
      },
      render: function render(context, env, contextualElement) {
        var dom = env.dom;
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
        return fragment;
      }
    };
  }());
  var child2 = (function() {
    var child0 = (function() {
      return {
        isHTMLBars: true,
        blockParams: 0,
        cachedFragment: null,
        hasRendered: false,
        build: function build(dom) {
          var el0 = dom.createDocumentFragment();
          var el1 = dom.createTextNode("						");
          dom.appendChild(el0, el1);
          var el1 = dom.createElement("li");
          dom.setAttribute(el1,"class","dropdown");
          var el2 = dom.createElement("a");
          dom.setAttribute(el2,"href","javascript:;");
          dom.setAttribute(el2,"class","dropdown-toggle");
          dom.setAttribute(el2,"data-toggle","collapse");
          dom.setAttribute(el2,"data-target","#cuenta");
          var el3 = dom.createElement("b");
          dom.setAttribute(el3,"class","caret");
          dom.appendChild(el2, el3);
          dom.appendChild(el1, el2);
          var el2 = dom.createTextNode("\n							");
          dom.appendChild(el1, el2);
          var el2 = dom.createElement("ul");
          dom.setAttribute(el2,"id","#cuenta");
          dom.setAttribute(el2,"class","collapse dropdown-menu");
          var el3 = dom.createTextNode("\n								");
          dom.appendChild(el2, el3);
          var el3 = dom.createElement("li");
          var el4 = dom.createElement("a");
          dom.setAttribute(el4,"href","/profile/teacher/teacher.id");
          var el5 = dom.createElement("span");
          dom.setAttribute(el5,"class","glyphicon glyphicon-user");
          dom.appendChild(el4, el5);
          var el5 = dom.createTextNode("  Perfil");
          dom.appendChild(el4, el5);
          dom.appendChild(el3, el4);
          dom.appendChild(el2, el3);
          var el3 = dom.createTextNode("\n								");
          dom.appendChild(el2, el3);
          var el3 = dom.createElement("li");
          var el4 = dom.createElement("a");
          dom.setAttribute(el4,"href","/account");
          var el5 = dom.createElement("span");
          dom.setAttribute(el5,"class","glyphicon glyphicon-cog");
          dom.appendChild(el4, el5);
          var el5 = dom.createTextNode("  Cuenta");
          dom.appendChild(el4, el5);
          dom.appendChild(el3, el4);
          dom.appendChild(el2, el3);
          var el3 = dom.createTextNode("\n								");
          dom.appendChild(el2, el3);
          var el3 = dom.createElement("li");
          var el4 = dom.createElement("a");
          dom.setAttribute(el4,"href","/messages");
          var el5 = dom.createElement("span");
          dom.setAttribute(el5,"class","glyphicon glyphicon-envelope");
          dom.appendChild(el4, el5);
          var el5 = dom.createTextNode("  Mensajes");
          dom.appendChild(el4, el5);
          dom.appendChild(el3, el4);
          dom.appendChild(el2, el3);
          var el3 = dom.createTextNode("\n							");
          dom.appendChild(el2, el3);
          dom.appendChild(el1, el2);
          var el2 = dom.createTextNode("\n						");
          dom.appendChild(el1, el2);
          dom.appendChild(el0, el1);
          var el1 = dom.createTextNode("\n");
          dom.appendChild(el0, el1);
          return el0;
        },
        render: function render(context, env, contextualElement) {
          var dom = env.dom;
          var hooks = env.hooks, content = hooks.content;
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
          var morph0 = dom.createMorphAt(dom.childAt(fragment, [1, 0]),-1,0);
          content(env, morph0, context, "teacher.name");
          return fragment;
        }
      };
    }());
    var child1 = (function() {
      return {
        isHTMLBars: true,
        blockParams: 0,
        cachedFragment: null,
        hasRendered: false,
        build: function build(dom) {
          var el0 = dom.createDocumentFragment();
          var el1 = dom.createTextNode("						");
          dom.appendChild(el0, el1);
          var el1 = dom.createElement("li");
          var el2 = dom.createTextNode("\n							");
          dom.appendChild(el1, el2);
          var el2 = dom.createElement("a");
          dom.setAttribute(el2,"href","/account");
          dom.appendChild(el1, el2);
          var el2 = dom.createTextNode("\n						");
          dom.appendChild(el1, el2);
          dom.appendChild(el0, el1);
          var el1 = dom.createTextNode("\n");
          dom.appendChild(el0, el1);
          return el0;
        },
        render: function render(context, env, contextualElement) {
          var dom = env.dom;
          var hooks = env.hooks, content = hooks.content;
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
          var morph0 = dom.createMorphAt(dom.childAt(fragment, [1, 1]),-1,-1);
          content(env, morph0, context, "user.name");
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
        var el1 = dom.createTextNode("					");
        dom.appendChild(el0, el1);
        var el1 = dom.createElement("li");
        var el2 = dom.createElement("a");
        dom.setAttribute(el2,"href","/logout");
        var el3 = dom.createTextNode("Salir");
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode("\n");
        dom.appendChild(el0, el1);
        return el0;
      },
      render: function render(context, env, contextualElement) {
        var dom = env.dom;
        var hooks = env.hooks, get = hooks.get, block = hooks.block;
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
        if (this.cachedFragment) { dom.repairClonedNode(fragment,[0]); }
        var morph0 = dom.createMorphAt(fragment,0,1,contextualElement);
        block(env, morph0, context, "if", [get(env, context, "teacher")], {}, child0, child1);
        return fragment;
      }
    };
  }());
  var child3 = (function() {
    return {
      isHTMLBars: true,
      blockParams: 0,
      cachedFragment: null,
      hasRendered: false,
      build: function build(dom) {
        var el0 = dom.createDocumentFragment();
        var el1 = dom.createTextNode("					");
        dom.appendChild(el0, el1);
        var el1 = dom.createElement("li");
        dom.setAttribute(el1,"class","dropdown");
        var el2 = dom.createElement("a");
        dom.setAttribute(el2,"href","#");
        dom.setAttribute(el2,"class","dropdown-toggle");
        dom.setAttribute(el2,"data-toggle","dropdown");
        var el3 = dom.createTextNode("Ingresar");
        dom.appendChild(el2, el3);
        var el3 = dom.createElement("b");
        dom.setAttribute(el3,"class","caret");
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        var el2 = dom.createTextNode("\n						");
        dom.appendChild(el1, el2);
        var el2 = dom.createElement("ul");
        dom.setAttribute(el2,"class","dropdown-menu min-width-200");
        var el3 = dom.createTextNode("\n							");
        dom.appendChild(el2, el3);
        var el3 = dom.createElement("li");
        var el4 = dom.createTextNode("\n								");
        dom.appendChild(el3, el4);
        var el4 = dom.createElement("a");
        var el5 = dom.createTextNode("\n									");
        dom.appendChild(el4, el5);
        var el5 = dom.createElement("form");
        dom.setAttribute(el5,"method","post");
        dom.setAttribute(el5,"action","/login");
        dom.setAttribute(el5,"role","form");
        dom.setAttribute(el5,"id","loginForm");
        var el6 = dom.createTextNode("\n										Ingresa con facebook\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("div");
        dom.setAttribute(el6,"class","center-block");
        var el7 = dom.createElement("fb:login-button");
        dom.setAttribute(el7,"scope","public_profile,email");
        dom.setAttribute(el7,"onlogin","checkLoginState();");
        dom.setAttribute(el7,"class","center-block text-center");
        var el8 = dom.createTextNode("\n										");
        dom.appendChild(el7, el8);
        dom.appendChild(el6, el7);
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("hr");
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n										Ingresa correo\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("div");
        dom.setAttribute(el6,"class","form-group");
        var el7 = dom.createTextNode("\n											");
        dom.appendChild(el6, el7);
        var el7 = dom.createElement("div");
        dom.setAttribute(el7,"class","input-group");
        var el8 = dom.createTextNode("\n												");
        dom.appendChild(el7, el8);
        var el8 = dom.createElement("div");
        dom.setAttribute(el8,"class","input-group-addon");
        var el9 = dom.createElement("span");
        dom.setAttribute(el9,"class","glyphicon glyphicon-envelope");
        dom.appendChild(el8, el9);
        dom.appendChild(el7, el8);
        var el8 = dom.createTextNode("\n												");
        dom.appendChild(el7, el8);
        var el8 = dom.createElement("input");
        dom.setAttribute(el8,"name","mail");
        dom.setAttribute(el8,"class","form-control");
        dom.setAttribute(el8,"type","email");
        dom.setAttribute(el8,"placeholder","email@domain.com");
        dom.setAttribute(el8,"id","mailLogin");
        dom.appendChild(el7, el8);
        var el8 = dom.createTextNode("\n											");
        dom.appendChild(el7, el8);
        dom.appendChild(el6, el7);
        var el7 = dom.createTextNode("\n											");
        dom.appendChild(el6, el7);
        var el7 = dom.createElement("p");
        dom.setAttribute(el7,"class","help-block");
        dom.appendChild(el6, el7);
        var el7 = dom.createTextNode("\n										");
        dom.appendChild(el6, el7);
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("div");
        dom.setAttribute(el6,"class","form-group");
        var el7 = dom.createTextNode("\n											");
        dom.appendChild(el6, el7);
        var el7 = dom.createElement("div");
        dom.setAttribute(el7,"class","input-group");
        var el8 = dom.createTextNode("\n												");
        dom.appendChild(el7, el8);
        var el8 = dom.createElement("div");
        dom.setAttribute(el8,"class","input-group-addon");
        var el9 = dom.createElement("span");
        dom.setAttribute(el9,"class","glyphicon glyphicon-lock");
        dom.appendChild(el8, el9);
        dom.appendChild(el7, el8);
        var el8 = dom.createTextNode("\n												");
        dom.appendChild(el7, el8);
        var el8 = dom.createElement("input");
        dom.setAttribute(el8,"name","pw");
        dom.setAttribute(el8,"class","form-control");
        dom.setAttribute(el8,"type","password");
        dom.appendChild(el7, el8);
        var el8 = dom.createTextNode("\n											");
        dom.appendChild(el7, el8);
        dom.appendChild(el6, el7);
        var el7 = dom.createTextNode("\n										");
        dom.appendChild(el6, el7);
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("div");
        dom.setAttribute(el6,"class","checkbox");
        var el7 = dom.createTextNode("\n											");
        dom.appendChild(el6, el7);
        var el7 = dom.createElement("input");
        dom.setAttribute(el7,"name","remember");
        dom.setAttribute(el7,"type","checkbox");
        dom.setAttribute(el7,"value","yes");
        dom.appendChild(el6, el7);
        var el7 = dom.createTextNode(" Recuerda\n										");
        dom.appendChild(el6, el7);
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("	\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("button");
        dom.setAttribute(el6,"type","submit");
        dom.setAttribute(el6,"class","btn btn-success");
        var el7 = dom.createTextNode("Ingresa");
        dom.appendChild(el6, el7);
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("br");
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n										");
        dom.appendChild(el5, el6);
        var el6 = dom.createElement("input");
        dom.setAttribute(el6,"type","hidden");
        dom.setAttribute(el6,"name","fbID");
        dom.setAttribute(el6,"id","fbIDLogin");
        dom.appendChild(el5, el6);
        var el6 = dom.createTextNode("\n									");
        dom.appendChild(el5, el6);
        dom.appendChild(el4, el5);
        var el5 = dom.createTextNode("\n								");
        dom.appendChild(el4, el5);
        dom.appendChild(el3, el4);
        var el4 = dom.createTextNode("\n							");
        dom.appendChild(el3, el4);
        dom.appendChild(el2, el3);
        var el3 = dom.createTextNode("\n						");
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        var el2 = dom.createTextNode("\n					");
        dom.appendChild(el1, el2);
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode("\n					");
        dom.appendChild(el0, el1);
        var el1 = dom.createElement("li");
        var el2 = dom.createElement("div");
        dom.setAttribute(el2,"id","register");
        var el3 = dom.createElement("a");
        dom.setAttribute(el3,"href","/signup");
        dom.setAttribute(el3,"id","aregister");
        var el4 = dom.createTextNode("Registrarse");
        dom.appendChild(el3, el4);
        dom.appendChild(el2, el3);
        dom.appendChild(el1, el2);
        dom.appendChild(el0, el1);
        var el1 = dom.createTextNode("\n");
        dom.appendChild(el0, el1);
        return el0;
      },
      render: function render(context, env, contextualElement) {
        var dom = env.dom;
        var hooks = env.hooks, content = hooks.content;
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
        var morph0 = dom.createMorphAt(dom.childAt(fragment, [1, 2, 1, 1, 1, 5, 3]),-1,-1);
        content(env, morph0, context, "error");
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
      var el1 = dom.createElement("nav");
      dom.setAttribute(el1,"class","navbar navbar-inverse navbar-fixed-top");
      dom.setAttribute(el1,"role","navigation");
      var el2 = dom.createTextNode("\n	");
      dom.appendChild(el1, el2);
      var el2 = dom.createElement("div");
      dom.setAttribute(el2,"class","container");
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("div");
      dom.setAttribute(el3,"class","navbar-header");
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("button");
      dom.setAttribute(el4,"type","button");
      dom.setAttribute(el4,"class","navbar-toggle");
      dom.setAttribute(el4,"data-toggle","collapse");
      dom.setAttribute(el4,"data-target","#teachme-navbar-collapse-1");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("span");
      dom.setAttribute(el5,"class","sr-only");
      var el6 = dom.createTextNode("Toggle navigation");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("span");
      dom.setAttribute(el5,"class","icon-bar");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("span");
      dom.setAttribute(el5,"class","icon-bar");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("span");
      dom.setAttribute(el5,"class","icon-bar");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("a");
      dom.setAttribute(el4,"class","navbar-brand navpos");
      dom.setAttribute(el4,"href","/");
      var el5 = dom.createElement("img");
      dom.setAttribute(el5,"src","/static/rsz_logo.png");
      dom.setAttribute(el5,"class","img-responsive");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n		");
      dom.appendChild(el3, el4);
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createComment(" Opciones de la barra del navegador ");
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("div");
      dom.setAttribute(el3,"class","collapse navbar-collapse");
      dom.setAttribute(el3,"id","teachme-navbar-collapse-1");
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("ul");
      dom.setAttribute(el4,"class","nav navbar-nav");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("li");
      dom.setAttribute(el5,"class","dropdown");
      var el6 = dom.createElement("a");
      dom.setAttribute(el6,"href","#");
      dom.setAttribute(el6,"class","dropdown-toggle");
      dom.setAttribute(el6,"data-toggle","dropdown");
      var el7 = dom.createTextNode("Aprende");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("b");
      dom.setAttribute(el7,"class","caret");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n					");
      dom.appendChild(el5, el6);
      var el6 = dom.createElement("ul");
      dom.setAttribute(el6,"class","dropdown-menu");
      var el7 = dom.createTextNode("\n						");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("li");
      var el8 = dom.createElement("a");
      dom.setAttribute(el8,"href","/aprende/a.id");
      dom.appendChild(el7, el8);
      dom.appendChild(el6, el7);
      var el7 = dom.createTextNode("\n					");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n				");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("form");
      dom.setAttribute(el4,"class","navbar-form navbar-left");
      dom.setAttribute(el4,"role","search");
      dom.setAttribute(el4,"action","/buscar/");
      dom.setAttribute(el4,"method","get");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("div");
      dom.setAttribute(el5,"class","form-group");
      var el6 = dom.createTextNode("\n					");
      dom.appendChild(el5, el6);
      var el6 = dom.createElement("input");
      dom.setAttribute(el6,"id","search_query");
      dom.setAttribute(el6,"name","q");
      dom.setAttribute(el6,"type","text");
      dom.setAttribute(el6,"class","form-control");
      dom.setAttribute(el6,"placeholder","Quiero aprender...");
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n				");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("button");
      dom.setAttribute(el5,"type","submit");
      dom.setAttribute(el5,"class","btn btn-primary");
      var el6 = dom.createElement("span");
      dom.setAttribute(el6,"class","glyphicon glyphicon-search");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("ul");
      dom.setAttribute(el4,"class","nav navbar-nav navbar-right");
      var el5 = dom.createTextNode("\n");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("li");
      dom.setAttribute(el5,"class","dropdown");
      var el6 = dom.createElement("a");
      dom.setAttribute(el6,"href","#");
      dom.setAttribute(el6,"class","dropdown-toggle");
      dom.setAttribute(el6,"data-toggle","dropdown");
      var el7 = dom.createElement("span");
      dom.setAttribute(el7,"class","flaticon-share11 font-25");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n					");
      dom.appendChild(el5, el6);
      var el6 = dom.createElement("ul");
      dom.setAttribute(el6,"class","dropdown-menu font-30");
      var el7 = dom.createTextNode("\n						");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("li");
      dom.setAttribute(el7,"class","dropdown-header text-center");
      var el8 = dom.createTextNode("Comparte");
      dom.appendChild(el7, el8);
      var el8 = dom.createElement("span");
      dom.setAttribute(el8,"class","flaticon-heart15");
      dom.appendChild(el7, el8);
      dom.appendChild(el6, el7);
      var el7 = dom.createTextNode("\n						");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("li");
      dom.setAttribute(el7,"class","text-center");
      var el8 = dom.createTextNode("\n							\n						");
      dom.appendChild(el7, el8);
      dom.appendChild(el6, el7);
      var el7 = dom.createTextNode("\n					");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n				");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("li");
      dom.setAttribute(el5,"class","dropdown");
      var el6 = dom.createElement("a");
      dom.setAttribute(el6,"href","#");
      dom.setAttribute(el6,"class","dropdown-toggle");
      dom.setAttribute(el6,"data-toggle","dropdown");
      var el7 = dom.createElement("small");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n					");
      dom.appendChild(el5, el6);
      var el6 = dom.createElement("ul");
      dom.setAttribute(el6,"class","dropdown-menu");
      var el7 = dom.createTextNode("\n						");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("li");
      var el8 = dom.createElement("form");
      dom.setAttribute(el8,"method","post");
      dom.setAttribute(el8,"action","/language");
      dom.setAttribute(el8,"role","form");
      var el9 = dom.createTextNode("\n							");
      dom.appendChild(el8, el9);
      var el9 = dom.createElement("input");
      dom.setAttribute(el9,"type","hidden");
      dom.setAttribute(el9,"name","locale");
      dom.setAttribute(el9,"value","en_US");
      dom.appendChild(el8, el9);
      var el9 = dom.createTextNode("\n							");
      dom.appendChild(el8, el9);
      var el9 = dom.createElement("button");
      dom.setAttribute(el9,"type","submit");
      dom.setAttribute(el9,"class","btn unstyled-btn");
      var el10 = dom.createTextNode("Inglés");
      dom.appendChild(el9, el10);
      dom.appendChild(el8, el9);
      var el9 = dom.createTextNode("\n						");
      dom.appendChild(el8, el9);
      dom.appendChild(el7, el8);
      dom.appendChild(el6, el7);
      var el7 = dom.createTextNode("\n							");
      dom.appendChild(el6, el7);
      var el7 = dom.createElement("li");
      var el8 = dom.createElement("form");
      dom.setAttribute(el8,"method","post");
      dom.setAttribute(el8,"action","/language");
      dom.setAttribute(el8,"role","form");
      var el9 = dom.createTextNode("\n							");
      dom.appendChild(el8, el9);
      var el9 = dom.createElement("input");
      dom.setAttribute(el9,"type","hidden");
      dom.setAttribute(el9,"name","locale");
      dom.setAttribute(el9,"value","es_ES");
      dom.appendChild(el8, el9);
      var el9 = dom.createTextNode("\n							");
      dom.appendChild(el8, el9);
      var el9 = dom.createElement("button");
      dom.setAttribute(el9,"type","submit");
      dom.setAttribute(el9,"class","btn unstyled-btn");
      var el10 = dom.createTextNode("Español");
      dom.appendChild(el9, el10);
      dom.appendChild(el8, el9);
      var el9 = dom.createTextNode("\n						");
      dom.appendChild(el8, el9);
      dom.appendChild(el7, el8);
      dom.appendChild(el6, el7);
      var el7 = dom.createTextNode("\n					");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      var el6 = dom.createTextNode("\n				");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n		");
      dom.appendChild(el3, el4);
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n	");
      dom.appendChild(el2, el3);
      dom.appendChild(el1, el2);
      var el2 = dom.createTextNode("\n");
      dom.appendChild(el1, el2);
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("\n");
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("\n");
      dom.appendChild(el0, el1);
      var el1 = dom.createElement("footer");
      var el2 = dom.createTextNode("\n	");
      dom.appendChild(el1, el2);
      var el2 = dom.createElement("div");
      dom.setAttribute(el2,"class","container");
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("div");
      dom.setAttribute(el3,"class","row");
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-3 text-center");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"href","/terminos");
      var el6 = dom.createElement("h4");
      var el7 = dom.createTextNode("Términos");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-3 text-center");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"href","/politicas");
      var el6 = dom.createElement("h4");
      var el7 = dom.createTextNode("Políticas");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-3 text-center");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"href","/faq");
      var el6 = dom.createElement("h4");
      var el7 = dom.createTextNode("FAQ");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-3 text-center");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("h4");
      var el6 = dom.createElement("a");
      dom.setAttribute(el6,"href","/contacto");
      var el7 = dom.createTextNode("Contacto");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n		");
      dom.appendChild(el3, el4);
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("div");
      dom.setAttribute(el3,"class","row");
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-12");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("hr");
      dom.setAttribute(el5,"class","hr");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("br");
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n		");
      dom.appendChild(el3, el4);
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("div");
      dom.setAttribute(el3,"class","row");
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-4 col-md-offset-4 text-center");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("p");
      var el6 = dom.createTextNode("Medellín - Colombia. ");
      dom.appendChild(el5, el6);
      var el6 = dom.createElement("a");
      dom.setAttribute(el6,"href","mailto:info@teachmeapp.com");
      var el7 = dom.createTextNode("info@teachmeapp.com");
      dom.appendChild(el6, el7);
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n			");
      dom.appendChild(el3, el4);
      var el4 = dom.createElement("div");
      dom.setAttribute(el4,"class","col-md-4 text-right");
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"target","_blank");
      dom.setAttribute(el5,"href","https://www.facebook.com/app.teachme");
      var el6 = dom.createElement("img");
      dom.setAttribute(el6,"src","/static/icons/facebookb.svg");
      dom.setAttribute(el6,"class","img-responsive inline img-35");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"target","_blank");
      dom.setAttribute(el5,"href","https://www.twitter.com/teachme_app");
      var el6 = dom.createElement("img");
      dom.setAttribute(el6,"src","/static/icons/twitterb.svg");
      dom.setAttribute(el6,"class","img-responsive inline img-35");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n				");
      dom.appendChild(el4, el5);
      var el5 = dom.createElement("a");
      dom.setAttribute(el5,"target","_blank");
      dom.setAttribute(el5,"href","https://www.youtube.com/channel/UCRfDpYrr9ix-rO8ZWwOqMgQ");
      var el6 = dom.createElement("img");
      dom.setAttribute(el6,"src","/static/icons/youtubeb.svg");
      dom.setAttribute(el6,"class","img-responsive inline img-35");
      dom.appendChild(el5, el6);
      dom.appendChild(el4, el5);
      var el5 = dom.createTextNode("\n			");
      dom.appendChild(el4, el5);
      dom.appendChild(el3, el4);
      var el4 = dom.createTextNode("\n		");
      dom.appendChild(el3, el4);
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n		");
      dom.appendChild(el2, el3);
      var el3 = dom.createElement("br");
      dom.appendChild(el2, el3);
      var el3 = dom.createTextNode("\n	");
      dom.appendChild(el2, el3);
      dom.appendChild(el1, el2);
      var el2 = dom.createTextNode("\n");
      dom.appendChild(el1, el2);
      dom.appendChild(el0, el1);
      var el1 = dom.createTextNode("\n");
      dom.appendChild(el0, el1);
      return el0;
    },
    render: function render(context, env, contextualElement) {
      var dom = env.dom;
      var hooks = env.hooks, content = hooks.content, get = hooks.get, block = hooks.block;
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
      var element0 = dom.childAt(fragment, [0, 1, 5]);
      var element1 = dom.childAt(element0, [1]);
      var element2 = dom.childAt(element0, [5]);
      if (this.cachedFragment) { dom.repairClonedNode(element2,[1]); }
      var morph0 = dom.createMorphAt(dom.childAt(element1, [1, 2, 1, 0]),-1,-1);
      var morph1 = dom.createMorphAt(element1,2,3);
      var morph2 = dom.createMorphAt(element2,0,1);
      var morph3 = dom.createMorphAt(element2,1,2);
      var morph4 = dom.createMorphAt(dom.childAt(element2, [5, 0, 0]),-1,-1);
      var morph5 = dom.createMorphAt(fragment,1,2,contextualElement);
      content(env, morph0, context, "a.name");
      block(env, morph1, context, "unless", [get(env, context, "teacher")], {}, child0, null);
      block(env, morph2, context, "if", [get(env, context, "user")], {}, child1, null);
      block(env, morph3, context, "if", [get(env, context, "user")], {}, child2, child3);
      content(env, morph4, context, "language");
      content(env, morph5, context, "outlet");
      return fragment;
    }
  };
}()));