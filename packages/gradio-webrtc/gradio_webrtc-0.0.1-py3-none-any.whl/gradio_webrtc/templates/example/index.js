var v;
(function(e) {
  e.LOAD = "LOAD", e.EXEC = "EXEC", e.WRITE_FILE = "WRITE_FILE", e.READ_FILE = "READ_FILE", e.DELETE_FILE = "DELETE_FILE", e.RENAME = "RENAME", e.CREATE_DIR = "CREATE_DIR", e.LIST_DIR = "LIST_DIR", e.DELETE_DIR = "DELETE_DIR", e.ERROR = "ERROR", e.DOWNLOAD = "DOWNLOAD", e.PROGRESS = "PROGRESS", e.LOG = "LOG", e.MOUNT = "MOUNT", e.UNMOUNT = "UNMOUNT";
})(v || (v = {}));
const {
  SvelteComponent: q,
  append: X,
  attr: D,
  binding_callbacks: T,
  detach: I,
  element: h,
  empty: w,
  init: j,
  insert: O,
  is_function: A,
  listen: L,
  noop: N,
  run_all: z,
  safe_not_equal: B,
  set_data: P,
  src_url_equal: k,
  text: Q,
  toggle_class: E
} = window.__gradio__svelte__internal;
function p(e) {
  let n;
  function t(f, i) {
    return H;
  }
  let o = t()(e);
  return {
    c() {
      o.c(), n = w();
    },
    m(f, i) {
      o.m(f, i), O(f, n, i);
    },
    p(f, i) {
      o.p(f, i);
    },
    d(f) {
      f && I(n), o.d(f);
    }
  };
}
function H(e) {
  let n, t, l, o, f;
  return {
    c() {
      var i;
      n = h("div"), t = h("video"), k(t.src, l = /*value*/
      (i = e[2]) == null ? void 0 : i.video.url) || D(t, "src", l), D(n, "class", "container svelte-13u05e4"), E(
        n,
        "table",
        /*type*/
        e[0] === "table"
      ), E(
        n,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), E(
        n,
        "selected",
        /*selected*/
        e[1]
      );
    },
    m(i, c) {
      O(i, n, c), X(n, t), e[6](t), o || (f = [
        L(
          t,
          "loadeddata",
          /*init*/
          e[4]
        ),
        L(t, "mouseover", function() {
          A(
            /*video*/
            e[3].play.bind(
              /*video*/
              e[3]
            )
          ) && e[3].play.bind(
            /*video*/
            e[3]
          ).apply(this, arguments);
        }),
        L(t, "mouseout", function() {
          A(
            /*video*/
            e[3].pause.bind(
              /*video*/
              e[3]
            )
          ) && e[3].pause.bind(
            /*video*/
            e[3]
          ).apply(this, arguments);
        })
      ], o = !0);
    },
    p(i, c) {
      var u;
      e = i, c & /*value*/
      4 && !k(t.src, l = /*value*/
      (u = e[2]) == null ? void 0 : u.video.url) && D(t, "src", l), c & /*type*/
      1 && E(
        n,
        "table",
        /*type*/
        e[0] === "table"
      ), c & /*type*/
      1 && E(
        n,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), c & /*selected*/
      2 && E(
        n,
        "selected",
        /*selected*/
        e[1]
      );
    },
    d(i) {
      i && I(n), e[6](null), o = !1, z(f);
    }
  };
}
function J(e) {
  let n, t = (
    /*value*/
    e[2] && p(e)
  );
  return {
    c() {
      t && t.c(), n = w();
    },
    m(l, o) {
      t && t.m(l, o), O(l, n, o);
    },
    p(l, [o]) {
      /*value*/
      l[2] ? t ? t.p(l, o) : (t = p(l), t.c(), t.m(n.parentNode, n)) : t && (t.d(1), t = null);
    },
    i: N,
    o: N,
    d(l) {
      l && I(n), t && t.d(l);
    }
  };
}
function K(e, n, t) {
  var l = this && this.__awaiter || function(_, U, a, s) {
    function C(d) {
      return d instanceof a ? d : new a(function(R) {
        R(d);
      });
    }
    return new (a || (a = Promise))(function(d, R) {
      function G(r) {
        try {
          b(s.next(r));
        } catch (m) {
          R(m);
        }
      }
      function W(r) {
        try {
          b(s.throw(r));
        } catch (m) {
          R(m);
        }
      }
      function b(r) {
        r.done ? d(r.value) : C(r.value).then(G, W);
      }
      b((s = s.apply(_, U || [])).next());
    });
  };
  let { type: o } = n, { selected: f = !1 } = n, { value: i } = n, { loop: c } = n, u;
  function y() {
    return l(this, void 0, void 0, function* () {
      t(3, u.muted = !0, u), t(3, u.playsInline = !0, u), t(3, u.controls = !1, u), u.setAttribute("muted", ""), yield u.play(), u.pause();
    });
  }
  function S(_) {
    T[_ ? "unshift" : "push"](() => {
      u = _, t(3, u);
    });
  }
  return e.$$set = (_) => {
    "type" in _ && t(0, o = _.type), "selected" in _ && t(1, f = _.selected), "value" in _ && t(2, i = _.value), "loop" in _ && t(5, c = _.loop);
  }, [o, f, i, u, y, c, S];
}
class V extends q {
  constructor(n) {
    super(), j(this, n, K, J, B, { type: 0, selected: 1, value: 2, loop: 5 });
  }
}
export {
  V as default
};
