const {
  SvelteComponent: Co,
  assign: Lo,
  create_slot: Ro,
  detach: Do,
  element: Io,
  get_all_dirty_from_scope: Oo,
  get_slot_changes: No,
  get_spread_update: Mo,
  init: Po,
  insert: Uo,
  safe_not_equal: Fo,
  set_dynamic_element_data: vi,
  set_style: J,
  toggle_class: Pe,
  transition_in: Bl,
  transition_out: Hl,
  update_slot_base: zo
} = window.__gradio__svelte__internal;
function qo(i) {
  let e, t, n;
  const l = (
    /*#slots*/
    i[21].default
  ), o = Ro(
    l,
    i,
    /*$$scope*/
    i[20],
    null
  );
  let r = [
    { "data-testid": (
      /*test_id*/
      i[9]
    ) },
    { id: (
      /*elem_id*/
      i[4]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      i[5].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let s = 0; s < r.length; s += 1)
    a = Lo(a, r[s]);
  return {
    c() {
      e = Io(
        /*tag*/
        i[17]
      ), o && o.c(), vi(
        /*tag*/
        i[17]
      )(e, a), Pe(
        e,
        "hidden",
        /*visible*/
        i[12] === !1
      ), Pe(
        e,
        "padded",
        /*padding*/
        i[8]
      ), Pe(
        e,
        "border_focus",
        /*border_mode*/
        i[7] === "focus"
      ), Pe(
        e,
        "border_contrast",
        /*border_mode*/
        i[7] === "contrast"
      ), Pe(e, "hide-container", !/*explicit_call*/
      i[10] && !/*container*/
      i[11]), J(
        e,
        "height",
        /*get_dimension*/
        i[18](
          /*height*/
          i[0]
        )
      ), J(
        e,
        "min-height",
        /*get_dimension*/
        i[18](
          /*min_height*/
          i[1]
        )
      ), J(
        e,
        "max-height",
        /*get_dimension*/
        i[18](
          /*max_height*/
          i[2]
        )
      ), J(e, "width", typeof /*width*/
      i[3] == "number" ? `calc(min(${/*width*/
      i[3]}px, 100%))` : (
        /*get_dimension*/
        i[18](
          /*width*/
          i[3]
        )
      )), J(
        e,
        "border-style",
        /*variant*/
        i[6]
      ), J(
        e,
        "overflow",
        /*allow_overflow*/
        i[13] ? (
          /*overflow_behavior*/
          i[14]
        ) : "hidden"
      ), J(
        e,
        "flex-grow",
        /*scale*/
        i[15]
      ), J(e, "min-width", `calc(min(${/*min_width*/
      i[16]}px, 100%))`), J(e, "border-width", "var(--block-border-width)");
    },
    m(s, f) {
      Uo(s, e, f), o && o.m(e, null), n = !0;
    },
    p(s, f) {
      o && o.p && (!n || f & /*$$scope*/
      1048576) && zo(
        o,
        l,
        s,
        /*$$scope*/
        s[20],
        n ? No(
          l,
          /*$$scope*/
          s[20],
          f,
          null
        ) : Oo(
          /*$$scope*/
          s[20]
        ),
        null
      ), vi(
        /*tag*/
        s[17]
      )(e, a = Mo(r, [
        (!n || f & /*test_id*/
        512) && { "data-testid": (
          /*test_id*/
          s[9]
        ) },
        (!n || f & /*elem_id*/
        16) && { id: (
          /*elem_id*/
          s[4]
        ) },
        (!n || f & /*elem_classes*/
        32 && t !== (t = "block " + /*elem_classes*/
        s[5].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Pe(
        e,
        "hidden",
        /*visible*/
        s[12] === !1
      ), Pe(
        e,
        "padded",
        /*padding*/
        s[8]
      ), Pe(
        e,
        "border_focus",
        /*border_mode*/
        s[7] === "focus"
      ), Pe(
        e,
        "border_contrast",
        /*border_mode*/
        s[7] === "contrast"
      ), Pe(e, "hide-container", !/*explicit_call*/
      s[10] && !/*container*/
      s[11]), f & /*height*/
      1 && J(
        e,
        "height",
        /*get_dimension*/
        s[18](
          /*height*/
          s[0]
        )
      ), f & /*min_height*/
      2 && J(
        e,
        "min-height",
        /*get_dimension*/
        s[18](
          /*min_height*/
          s[1]
        )
      ), f & /*max_height*/
      4 && J(
        e,
        "max-height",
        /*get_dimension*/
        s[18](
          /*max_height*/
          s[2]
        )
      ), f & /*width*/
      8 && J(e, "width", typeof /*width*/
      s[3] == "number" ? `calc(min(${/*width*/
      s[3]}px, 100%))` : (
        /*get_dimension*/
        s[18](
          /*width*/
          s[3]
        )
      )), f & /*variant*/
      64 && J(
        e,
        "border-style",
        /*variant*/
        s[6]
      ), f & /*allow_overflow, overflow_behavior*/
      24576 && J(
        e,
        "overflow",
        /*allow_overflow*/
        s[13] ? (
          /*overflow_behavior*/
          s[14]
        ) : "hidden"
      ), f & /*scale*/
      32768 && J(
        e,
        "flex-grow",
        /*scale*/
        s[15]
      ), f & /*min_width*/
      65536 && J(e, "min-width", `calc(min(${/*min_width*/
      s[16]}px, 100%))`);
    },
    i(s) {
      n || (Bl(o, s), n = !0);
    },
    o(s) {
      Hl(o, s), n = !1;
    },
    d(s) {
      s && Do(e), o && o.d(s);
    }
  };
}
function Bo(i) {
  let e, t = (
    /*tag*/
    i[17] && qo(i)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, l) {
      t && t.m(n, l), e = !0;
    },
    p(n, [l]) {
      /*tag*/
      n[17] && t.p(n, l);
    },
    i(n) {
      e || (Bl(t, n), e = !0);
    },
    o(n) {
      Hl(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Ho(i, e, t) {
  let { $$slots: n = {}, $$scope: l } = e, { height: o = void 0 } = e, { min_height: r = void 0 } = e, { max_height: a = void 0 } = e, { width: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: c = [] } = e, { variant: _ = "solid" } = e, { border_mode: d = "base" } = e, { padding: m = !0 } = e, { type: w = "normal" } = e, { test_id: E = void 0 } = e, { explicit_call: k = !1 } = e, { container: p = !0 } = e, { visible: L = !0 } = e, { allow_overflow: b = !0 } = e, { overflow_behavior: h = "auto" } = e, { scale: N = null } = e, { min_width: M = 0 } = e, H = w === "fieldset" ? "fieldset" : "div";
  const j = (S) => {
    if (S !== void 0) {
      if (typeof S == "number")
        return S + "px";
      if (typeof S == "string")
        return S;
    }
  };
  return i.$$set = (S) => {
    "height" in S && t(0, o = S.height), "min_height" in S && t(1, r = S.min_height), "max_height" in S && t(2, a = S.max_height), "width" in S && t(3, s = S.width), "elem_id" in S && t(4, f = S.elem_id), "elem_classes" in S && t(5, c = S.elem_classes), "variant" in S && t(6, _ = S.variant), "border_mode" in S && t(7, d = S.border_mode), "padding" in S && t(8, m = S.padding), "type" in S && t(19, w = S.type), "test_id" in S && t(9, E = S.test_id), "explicit_call" in S && t(10, k = S.explicit_call), "container" in S && t(11, p = S.container), "visible" in S && t(12, L = S.visible), "allow_overflow" in S && t(13, b = S.allow_overflow), "overflow_behavior" in S && t(14, h = S.overflow_behavior), "scale" in S && t(15, N = S.scale), "min_width" in S && t(16, M = S.min_width), "$$scope" in S && t(20, l = S.$$scope);
  }, [
    o,
    r,
    a,
    s,
    f,
    c,
    _,
    d,
    m,
    E,
    k,
    p,
    L,
    b,
    h,
    N,
    M,
    H,
    j,
    w,
    l,
    n
  ];
}
class jo extends Co {
  constructor(e) {
    super(), Po(this, e, Ho, Bo, Fo, {
      height: 0,
      min_height: 1,
      max_height: 2,
      width: 3,
      elem_id: 4,
      elem_classes: 5,
      variant: 6,
      border_mode: 7,
      padding: 8,
      type: 19,
      test_id: 9,
      explicit_call: 10,
      container: 11,
      visible: 12,
      allow_overflow: 13,
      overflow_behavior: 14,
      scale: 15,
      min_width: 16
    });
  }
}
const {
  SvelteComponent: Go,
  append: hn,
  attr: qt,
  create_component: Wo,
  destroy_component: Vo,
  detach: Yo,
  element: ki,
  init: Xo,
  insert: Zo,
  mount_component: Ko,
  safe_not_equal: Jo,
  set_data: Qo,
  space: xo,
  text: $o,
  toggle_class: Xe,
  transition_in: er,
  transition_out: tr
} = window.__gradio__svelte__internal;
function nr(i) {
  let e, t, n, l, o, r;
  return n = new /*Icon*/
  i[1]({}), {
    c() {
      e = ki("label"), t = ki("span"), Wo(n.$$.fragment), l = xo(), o = $o(
        /*label*/
        i[0]
      ), qt(t, "class", "svelte-9gxdi0"), qt(e, "for", ""), qt(e, "data-testid", "block-label"), qt(e, "class", "svelte-9gxdi0"), Xe(e, "hide", !/*show_label*/
      i[2]), Xe(e, "sr-only", !/*show_label*/
      i[2]), Xe(
        e,
        "float",
        /*float*/
        i[4]
      ), Xe(
        e,
        "hide-label",
        /*disable*/
        i[3]
      );
    },
    m(a, s) {
      Zo(a, e, s), hn(e, t), Ko(n, t, null), hn(e, l), hn(e, o), r = !0;
    },
    p(a, [s]) {
      (!r || s & /*label*/
      1) && Qo(
        o,
        /*label*/
        a[0]
      ), (!r || s & /*show_label*/
      4) && Xe(e, "hide", !/*show_label*/
      a[2]), (!r || s & /*show_label*/
      4) && Xe(e, "sr-only", !/*show_label*/
      a[2]), (!r || s & /*float*/
      16) && Xe(
        e,
        "float",
        /*float*/
        a[4]
      ), (!r || s & /*disable*/
      8) && Xe(
        e,
        "hide-label",
        /*disable*/
        a[3]
      );
    },
    i(a) {
      r || (er(n.$$.fragment, a), r = !0);
    },
    o(a) {
      tr(n.$$.fragment, a), r = !1;
    },
    d(a) {
      a && Yo(e), Vo(n);
    }
  };
}
function ir(i, e, t) {
  let { label: n = null } = e, { Icon: l } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: a = !0 } = e;
  return i.$$set = (s) => {
    "label" in s && t(0, n = s.label), "Icon" in s && t(1, l = s.Icon), "show_label" in s && t(2, o = s.show_label), "disable" in s && t(3, r = s.disable), "float" in s && t(4, a = s.float);
  }, [n, l, o, r, a];
}
class lr extends Go {
  constructor(e) {
    super(), Xo(this, e, ir, nr, Jo, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: or,
  append: qn,
  attr: He,
  bubble: rr,
  check_outros: sr,
  construct_svelte_component: Ei,
  create_component: Ti,
  destroy_component: yi,
  detach: jl,
  element: Bn,
  group_outros: ar,
  init: fr,
  insert: Gl,
  listen: cr,
  mount_component: Ai,
  safe_not_equal: ur,
  set_data: _r,
  set_style: Bt,
  space: dr,
  text: mr,
  toggle_class: ae,
  transition_in: Si,
  transition_out: Ci
} = window.__gradio__svelte__internal;
function Li(i) {
  let e, t;
  return {
    c() {
      e = Bn("span"), t = mr(
        /*label*/
        i[1]
      ), He(e, "class", "svelte-vk34kx");
    },
    m(n, l) {
      Gl(n, e, l), qn(e, t);
    },
    p(n, l) {
      l & /*label*/
      2 && _r(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && jl(e);
    }
  };
}
function hr(i) {
  let e, t, n, l, o, r, a, s = (
    /*show_label*/
    i[2] && Li(i)
  );
  var f = (
    /*Icon*/
    i[0]
  );
  function c(_, d) {
    return {};
  }
  return f && (l = Ei(f, c())), {
    c() {
      e = Bn("button"), s && s.c(), t = dr(), n = Bn("div"), l && Ti(l.$$.fragment), He(n, "class", "svelte-vk34kx"), ae(
        n,
        "small",
        /*size*/
        i[4] === "small"
      ), ae(
        n,
        "large",
        /*size*/
        i[4] === "large"
      ), ae(
        n,
        "medium",
        /*size*/
        i[4] === "medium"
      ), e.disabled = /*disabled*/
      i[7], He(
        e,
        "aria-label",
        /*label*/
        i[1]
      ), He(
        e,
        "aria-haspopup",
        /*hasPopup*/
        i[8]
      ), He(
        e,
        "title",
        /*label*/
        i[1]
      ), He(e, "class", "svelte-vk34kx"), ae(
        e,
        "pending",
        /*pending*/
        i[3]
      ), ae(
        e,
        "padded",
        /*padded*/
        i[5]
      ), ae(
        e,
        "highlight",
        /*highlight*/
        i[6]
      ), ae(
        e,
        "transparent",
        /*transparent*/
        i[9]
      ), Bt(e, "color", !/*disabled*/
      i[7] && /*_color*/
      i[11] ? (
        /*_color*/
        i[11]
      ) : "var(--block-label-text-color)"), Bt(e, "--bg-color", /*disabled*/
      i[7] ? "auto" : (
        /*background*/
        i[10]
      ));
    },
    m(_, d) {
      Gl(_, e, d), s && s.m(e, null), qn(e, t), qn(e, n), l && Ai(l, n, null), o = !0, r || (a = cr(
        e,
        "click",
        /*click_handler*/
        i[13]
      ), r = !0);
    },
    p(_, [d]) {
      if (/*show_label*/
      _[2] ? s ? s.p(_, d) : (s = Li(_), s.c(), s.m(e, t)) : s && (s.d(1), s = null), d & /*Icon*/
      1 && f !== (f = /*Icon*/
      _[0])) {
        if (l) {
          ar();
          const m = l;
          Ci(m.$$.fragment, 1, 0, () => {
            yi(m, 1);
          }), sr();
        }
        f ? (l = Ei(f, c()), Ti(l.$$.fragment), Si(l.$$.fragment, 1), Ai(l, n, null)) : l = null;
      }
      (!o || d & /*size*/
      16) && ae(
        n,
        "small",
        /*size*/
        _[4] === "small"
      ), (!o || d & /*size*/
      16) && ae(
        n,
        "large",
        /*size*/
        _[4] === "large"
      ), (!o || d & /*size*/
      16) && ae(
        n,
        "medium",
        /*size*/
        _[4] === "medium"
      ), (!o || d & /*disabled*/
      128) && (e.disabled = /*disabled*/
      _[7]), (!o || d & /*label*/
      2) && He(
        e,
        "aria-label",
        /*label*/
        _[1]
      ), (!o || d & /*hasPopup*/
      256) && He(
        e,
        "aria-haspopup",
        /*hasPopup*/
        _[8]
      ), (!o || d & /*label*/
      2) && He(
        e,
        "title",
        /*label*/
        _[1]
      ), (!o || d & /*pending*/
      8) && ae(
        e,
        "pending",
        /*pending*/
        _[3]
      ), (!o || d & /*padded*/
      32) && ae(
        e,
        "padded",
        /*padded*/
        _[5]
      ), (!o || d & /*highlight*/
      64) && ae(
        e,
        "highlight",
        /*highlight*/
        _[6]
      ), (!o || d & /*transparent*/
      512) && ae(
        e,
        "transparent",
        /*transparent*/
        _[9]
      ), d & /*disabled, _color*/
      2176 && Bt(e, "color", !/*disabled*/
      _[7] && /*_color*/
      _[11] ? (
        /*_color*/
        _[11]
      ) : "var(--block-label-text-color)"), d & /*disabled, background*/
      1152 && Bt(e, "--bg-color", /*disabled*/
      _[7] ? "auto" : (
        /*background*/
        _[10]
      ));
    },
    i(_) {
      o || (l && Si(l.$$.fragment, _), o = !0);
    },
    o(_) {
      l && Ci(l.$$.fragment, _), o = !1;
    },
    d(_) {
      _ && jl(e), s && s.d(), l && yi(l), r = !1, a();
    }
  };
}
function gr(i, e, t) {
  let n, { Icon: l } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: a = !1 } = e, { size: s = "small" } = e, { padded: f = !0 } = e, { highlight: c = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: d = !1 } = e, { color: m = "var(--block-label-text-color)" } = e, { transparent: w = !1 } = e, { background: E = "var(--block-background-fill)" } = e;
  function k(p) {
    rr.call(this, i, p);
  }
  return i.$$set = (p) => {
    "Icon" in p && t(0, l = p.Icon), "label" in p && t(1, o = p.label), "show_label" in p && t(2, r = p.show_label), "pending" in p && t(3, a = p.pending), "size" in p && t(4, s = p.size), "padded" in p && t(5, f = p.padded), "highlight" in p && t(6, c = p.highlight), "disabled" in p && t(7, _ = p.disabled), "hasPopup" in p && t(8, d = p.hasPopup), "color" in p && t(12, m = p.color), "transparent" in p && t(9, w = p.transparent), "background" in p && t(10, E = p.background);
  }, i.$$.update = () => {
    i.$$.dirty & /*highlight, color*/
    4160 && t(11, n = c ? "var(--color-accent)" : m);
  }, [
    l,
    o,
    r,
    a,
    s,
    f,
    c,
    _,
    d,
    w,
    E,
    n,
    m,
    k
  ];
}
class pr extends or {
  constructor(e) {
    super(), fr(this, e, gr, hr, ur, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 12,
      transparent: 9,
      background: 10
    });
  }
}
const {
  SvelteComponent: br,
  append: wr,
  attr: ke,
  detach: vr,
  init: kr,
  insert: Er,
  noop: gn,
  safe_not_equal: Tr,
  svg_element: Ri
} = window.__gradio__svelte__internal;
function yr(i) {
  let e, t;
  return {
    c() {
      e = Ri("svg"), t = Ri("circle"), ke(t, "cx", "12"), ke(t, "cy", "12"), ke(t, "r", "10"), ke(e, "xmlns", "http://www.w3.org/2000/svg"), ke(e, "width", "100%"), ke(e, "height", "100%"), ke(e, "viewBox", "0 0 24 24"), ke(e, "stroke-width", "1.5"), ke(e, "stroke-linecap", "round"), ke(e, "stroke-linejoin", "round"), ke(e, "class", "feather feather-circle");
    },
    m(n, l) {
      Er(n, e, l), wr(e, t);
    },
    p: gn,
    i: gn,
    o: gn,
    d(n) {
      n && vr(e);
    }
  };
}
class Ar extends br {
  constructor(e) {
    super(), kr(this, e, null, yr, Tr, {});
  }
}
const {
  SvelteComponent: Sr,
  append: pn,
  attr: Ee,
  detach: Cr,
  init: Lr,
  insert: Rr,
  noop: bn,
  safe_not_equal: Dr,
  set_style: Ue,
  svg_element: Ht
} = window.__gradio__svelte__internal;
function Ir(i) {
  let e, t, n, l;
  return {
    c() {
      e = Ht("svg"), t = Ht("g"), n = Ht("path"), l = Ht("path"), Ee(n, "d", "M18,6L6.087,17.913"), Ue(n, "fill", "none"), Ue(n, "fill-rule", "nonzero"), Ue(n, "stroke-width", "2px"), Ee(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Ee(l, "d", "M4.364,4.364L19.636,19.636"), Ue(l, "fill", "none"), Ue(l, "fill-rule", "nonzero"), Ue(l, "stroke-width", "2px"), Ee(e, "width", "100%"), Ee(e, "height", "100%"), Ee(e, "viewBox", "0 0 24 24"), Ee(e, "version", "1.1"), Ee(e, "xmlns", "http://www.w3.org/2000/svg"), Ee(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Ee(e, "xml:space", "preserve"), Ee(e, "stroke", "currentColor"), Ue(e, "fill-rule", "evenodd"), Ue(e, "clip-rule", "evenodd"), Ue(e, "stroke-linecap", "round"), Ue(e, "stroke-linejoin", "round");
    },
    m(o, r) {
      Rr(o, e, r), pn(e, t), pn(t, n), pn(e, l);
    },
    p: bn,
    i: bn,
    o: bn,
    d(o) {
      o && Cr(e);
    }
  };
}
class Or extends Sr {
  constructor(e) {
    super(), Lr(this, e, null, Ir, Dr, {});
  }
}
const {
  SvelteComponent: Nr,
  append: Mr,
  attr: dt,
  detach: Pr,
  init: Ur,
  insert: Fr,
  noop: wn,
  safe_not_equal: zr,
  svg_element: Di
} = window.__gradio__svelte__internal;
function qr(i) {
  let e, t;
  return {
    c() {
      e = Di("svg"), t = Di("path"), dt(t, "d", "M5 8l4 4 4-4z"), dt(e, "class", "dropdown-arrow svelte-145leq6"), dt(e, "xmlns", "http://www.w3.org/2000/svg"), dt(e, "width", "100%"), dt(e, "height", "100%"), dt(e, "viewBox", "0 0 18 18");
    },
    m(n, l) {
      Fr(n, e, l), Mr(e, t);
    },
    p: wn,
    i: wn,
    o: wn,
    d(n) {
      n && Pr(e);
    }
  };
}
class Wl extends Nr {
  constructor(e) {
    super(), Ur(this, e, null, qr, zr, {});
  }
}
const {
  SvelteComponent: Br,
  append: Hr,
  attr: jt,
  detach: jr,
  init: Gr,
  insert: Wr,
  noop: vn,
  safe_not_equal: Vr,
  svg_element: Ii
} = window.__gradio__svelte__internal;
function Yr(i) {
  let e, t;
  return {
    c() {
      e = Ii("svg"), t = Ii("path"), jt(t, "fill", "currentColor"), jt(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), jt(e, "xmlns", "http://www.w3.org/2000/svg"), jt(e, "viewBox", "0 0 24 24");
    },
    m(n, l) {
      Wr(n, e, l), Hr(e, t);
    },
    p: vn,
    i: vn,
    o: vn,
    d(n) {
      n && jr(e);
    }
  };
}
class Xr extends Br {
  constructor(e) {
    super(), Gr(this, e, null, Yr, Vr, {});
  }
}
const {
  SvelteComponent: Zr,
  append: Kr,
  attr: X,
  detach: Jr,
  init: Qr,
  insert: xr,
  noop: Oi,
  safe_not_equal: $r,
  svg_element: Ni
} = window.__gradio__svelte__internal;
function es(i) {
  let e, t, n;
  return {
    c() {
      e = Ni("svg"), t = Ni("rect"), X(t, "x", "3"), X(t, "y", "3"), X(t, "width", "18"), X(t, "height", "18"), X(t, "rx", "2"), X(t, "ry", "2"), X(e, "xmlns", "http://www.w3.org/2000/svg"), X(e, "width", "100%"), X(e, "height", "100%"), X(e, "viewBox", "0 0 24 24"), X(
        e,
        "fill",
        /*fill*/
        i[0]
      ), X(e, "stroke", "currentColor"), X(e, "stroke-width", n = `${/*stroke_width*/
      i[1]}`), X(e, "stroke-linecap", "round"), X(e, "stroke-linejoin", "round"), X(e, "class", "feather feather-square");
    },
    m(l, o) {
      xr(l, e, o), Kr(e, t);
    },
    p(l, [o]) {
      o & /*fill*/
      1 && X(
        e,
        "fill",
        /*fill*/
        l[0]
      ), o & /*stroke_width*/
      2 && n !== (n = `${/*stroke_width*/
      l[1]}`) && X(e, "stroke-width", n);
    },
    i: Oi,
    o: Oi,
    d(l) {
      l && Jr(e);
    }
  };
}
function ts(i, e, t) {
  let { fill: n = "currentColor" } = e, { stroke_width: l = 1.5 } = e;
  return i.$$set = (o) => {
    "fill" in o && t(0, n = o.fill), "stroke_width" in o && t(1, l = o.stroke_width);
  }, [n, l];
}
class ns extends Zr {
  constructor(e) {
    super(), Qr(this, e, ts, es, $r, { fill: 0, stroke_width: 1 });
  }
}
const {
  SvelteComponent: is,
  append: kn,
  attr: ee,
  detach: ls,
  init: os,
  insert: rs,
  noop: En,
  safe_not_equal: ss,
  svg_element: Gt
} = window.__gradio__svelte__internal;
function as(i) {
  let e, t, n, l;
  return {
    c() {
      e = Gt("svg"), t = Gt("path"), n = Gt("polyline"), l = Gt("line"), ee(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), ee(n, "points", "17 8 12 3 7 8"), ee(l, "x1", "12"), ee(l, "y1", "3"), ee(l, "x2", "12"), ee(l, "y2", "15"), ee(e, "xmlns", "http://www.w3.org/2000/svg"), ee(e, "width", "90%"), ee(e, "height", "90%"), ee(e, "viewBox", "0 0 24 24"), ee(e, "fill", "none"), ee(e, "stroke", "currentColor"), ee(e, "stroke-width", "2"), ee(e, "stroke-linecap", "round"), ee(e, "stroke-linejoin", "round"), ee(e, "class", "feather feather-upload");
    },
    m(o, r) {
      rs(o, e, r), kn(e, t), kn(e, n), kn(e, l);
    },
    p: En,
    i: En,
    o: En,
    d(o) {
      o && ls(e);
    }
  };
}
class fs extends is {
  constructor(e) {
    super(), os(this, e, null, as, ss, {});
  }
}
const {
  SvelteComponent: cs,
  append: Mi,
  attr: Q,
  detach: us,
  init: _s,
  insert: ds,
  noop: Tn,
  safe_not_equal: ms,
  svg_element: yn
} = window.__gradio__svelte__internal;
function hs(i) {
  let e, t, n;
  return {
    c() {
      e = yn("svg"), t = yn("polygon"), n = yn("rect"), Q(t, "points", "23 7 16 12 23 17 23 7"), Q(n, "x", "1"), Q(n, "y", "5"), Q(n, "width", "15"), Q(n, "height", "14"), Q(n, "rx", "2"), Q(n, "ry", "2"), Q(e, "xmlns", "http://www.w3.org/2000/svg"), Q(e, "width", "100%"), Q(e, "height", "100%"), Q(e, "viewBox", "0 0 24 24"), Q(e, "fill", "none"), Q(e, "stroke", "currentColor"), Q(e, "stroke-width", "1.5"), Q(e, "stroke-linecap", "round"), Q(e, "stroke-linejoin", "round"), Q(e, "class", "feather feather-video");
    },
    m(l, o) {
      ds(l, e, o), Mi(e, t), Mi(e, n);
    },
    p: Tn,
    i: Tn,
    o: Tn,
    d(l) {
      l && us(e);
    }
  };
}
class gs extends cs {
  constructor(e) {
    super(), _s(this, e, null, hs, ms, {});
  }
}
const {
  SvelteComponent: ps,
  append: Pi,
  attr: Ze,
  detach: bs,
  init: ws,
  insert: vs,
  noop: An,
  safe_not_equal: ks,
  svg_element: Sn
} = window.__gradio__svelte__internal;
function Es(i) {
  let e, t, n;
  return {
    c() {
      e = Sn("svg"), t = Sn("path"), n = Sn("path"), Ze(t, "fill", "currentColor"), Ze(t, "d", "M12 2c-4.963 0-9 4.038-9 9c0 3.328 1.82 6.232 4.513 7.79l-2.067 1.378A1 1 0 0 0 6 22h12a1 1 0 0 0 .555-1.832l-2.067-1.378C19.18 17.232 21 14.328 21 11c0-4.962-4.037-9-9-9zm0 16c-3.859 0-7-3.141-7-7c0-3.86 3.141-7 7-7s7 3.14 7 7c0 3.859-3.141 7-7 7z"), Ze(n, "fill", "currentColor"), Ze(n, "d", "M12 6c-2.757 0-5 2.243-5 5s2.243 5 5 5s5-2.243 5-5s-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3s3 1.346 3 3s-1.346 3-3 3z"), Ze(e, "xmlns", "http://www.w3.org/2000/svg"), Ze(e, "width", "100%"), Ze(e, "height", "100%"), Ze(e, "viewBox", "0 0 24 24");
    },
    m(l, o) {
      vs(l, e, o), Pi(e, t), Pi(e, n);
    },
    p: An,
    i: An,
    o: An,
    d(l) {
      l && bs(e);
    }
  };
}
let Ts = class extends ps {
  constructor(e) {
    super(), ws(this, e, null, Es, ks, {});
  }
};
const {
  SvelteComponent: ys,
  append: Ui,
  attr: Z,
  detach: As,
  init: Ss,
  insert: Cs,
  noop: Cn,
  safe_not_equal: Ls,
  svg_element: Ln
} = window.__gradio__svelte__internal;
function Rs(i) {
  let e, t, n;
  return {
    c() {
      e = Ln("svg"), t = Ln("circle"), n = Ln("animateTransform"), Z(n, "attributeName", "transform"), Z(n, "type", "rotate"), Z(n, "from", "0 25 25"), Z(n, "to", "360 25 25"), Z(n, "repeatCount", "indefinite"), Z(t, "cx", "25"), Z(t, "cy", "25"), Z(t, "r", "20"), Z(t, "fill", "none"), Z(t, "stroke-width", "3.0"), Z(t, "stroke-linecap", "round"), Z(t, "stroke-dasharray", "94.2477796076938 94.2477796076938"), Z(t, "stroke-dashoffset", "0"), Z(e, "xmlns", "http://www.w3.org/2000/svg"), Z(e, "width", "100%"), Z(e, "height", "100%"), Z(e, "viewBox", "0 0 50 50"), Z(e, "class", "svelte-pb9pol");
    },
    m(l, o) {
      Cs(l, e, o), Ui(e, t), Ui(t, n);
    },
    p: Cn,
    i: Cn,
    o: Cn,
    d(l) {
      l && As(e);
    }
  };
}
class Ds extends ys {
  constructor(e) {
    super(), Ss(this, e, null, Rs, Ls, {});
  }
}
const Is = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Fi = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Is.reduce(
  (i, { color: e, primary: t, secondary: n }) => ({
    ...i,
    [e]: {
      primary: Fi[e][t],
      secondary: Fi[e][n]
    }
  }),
  {}
);
const Os = /^(#\s*)(.+)$/m;
function Ns(i) {
  const e = i.trim(), t = e.match(Os);
  if (!t)
    return [!1, e || !1];
  const [n, , l] = t, o = l.trim();
  if (e === n)
    return [o, !1];
  const r = t.index !== void 0 ? t.index + n.length : 0, s = e.substring(r).trim() || !1;
  return [o, s];
}
const {
  SvelteComponent: Ms,
  append: it,
  attr: Rt,
  check_outros: Ps,
  create_component: Vl,
  destroy_component: Yl,
  detach: Le,
  element: Dt,
  empty: Xl,
  group_outros: Us,
  init: Fs,
  insert: Re,
  mount_component: Zl,
  safe_not_equal: zs,
  set_data: It,
  space: fn,
  text: tt,
  toggle_class: zi,
  transition_in: $t,
  transition_out: en
} = window.__gradio__svelte__internal;
function qs(i) {
  let e, t;
  return e = new fs({}), {
    c() {
      Vl(e.$$.fragment);
    },
    m(n, l) {
      Zl(e, n, l), t = !0;
    },
    i(n) {
      t || ($t(e.$$.fragment, n), t = !0);
    },
    o(n) {
      en(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Yl(e, n);
    }
  };
}
function Bs(i) {
  let e, t;
  return e = new Xr({}), {
    c() {
      Vl(e.$$.fragment);
    },
    m(n, l) {
      Zl(e, n, l), t = !0;
    },
    i(n) {
      t || ($t(e.$$.fragment, n), t = !0);
    },
    o(n) {
      en(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Yl(e, n);
    }
  };
}
function Hs(i) {
  let e = (
    /*i18n*/
    i[1](
      /*defs*/
      i[7][
        /*type*/
        i[0]
      ] || /*defs*/
      i[7].file
    ) + ""
  ), t, n, l, o = (
    /*mode*/
    i[3] !== "short" && qi(i)
  );
  return {
    c() {
      t = tt(e), n = fn(), o && o.c(), l = Xl();
    },
    m(r, a) {
      Re(r, t, a), Re(r, n, a), o && o.m(r, a), Re(r, l, a);
    },
    p(r, a) {
      a & /*i18n, type*/
      3 && e !== (e = /*i18n*/
      r[1](
        /*defs*/
        r[7][
          /*type*/
          r[0]
        ] || /*defs*/
        r[7].file
      ) + "") && It(t, e), /*mode*/
      r[3] !== "short" ? o ? o.p(r, a) : (o = qi(r), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null);
    },
    d(r) {
      r && (Le(t), Le(n), Le(l)), o && o.d(r);
    }
  };
}
function js(i) {
  let e, t, n = (
    /*heading*/
    i[6] && Bi(i)
  ), l = (
    /*paragraph*/
    i[5] && Hi(i)
  );
  return {
    c() {
      n && n.c(), e = fn(), l && l.c(), t = Xl();
    },
    m(o, r) {
      n && n.m(o, r), Re(o, e, r), l && l.m(o, r), Re(o, t, r);
    },
    p(o, r) {
      /*heading*/
      o[6] ? n ? n.p(o, r) : (n = Bi(o), n.c(), n.m(e.parentNode, e)) : n && (n.d(1), n = null), /*paragraph*/
      o[5] ? l ? l.p(o, r) : (l = Hi(o), l.c(), l.m(t.parentNode, t)) : l && (l.d(1), l = null);
    },
    d(o) {
      o && (Le(e), Le(t)), n && n.d(o), l && l.d(o);
    }
  };
}
function qi(i) {
  let e, t, n = (
    /*i18n*/
    i[1]("common.or") + ""
  ), l, o, r, a = (
    /*message*/
    (i[2] || /*i18n*/
    i[1]("upload_text.click_to_upload")) + ""
  ), s;
  return {
    c() {
      e = Dt("span"), t = tt("- "), l = tt(n), o = tt(" -"), r = fn(), s = tt(a), Rt(e, "class", "or svelte-1xg7h5n");
    },
    m(f, c) {
      Re(f, e, c), it(e, t), it(e, l), it(e, o), Re(f, r, c), Re(f, s, c);
    },
    p(f, c) {
      c & /*i18n*/
      2 && n !== (n = /*i18n*/
      f[1]("common.or") + "") && It(l, n), c & /*message, i18n*/
      6 && a !== (a = /*message*/
      (f[2] || /*i18n*/
      f[1]("upload_text.click_to_upload")) + "") && It(s, a);
    },
    d(f) {
      f && (Le(e), Le(r), Le(s));
    }
  };
}
function Bi(i) {
  let e, t;
  return {
    c() {
      e = Dt("h2"), t = tt(
        /*heading*/
        i[6]
      ), Rt(e, "class", "svelte-1xg7h5n");
    },
    m(n, l) {
      Re(n, e, l), it(e, t);
    },
    p(n, l) {
      l & /*heading*/
      64 && It(
        t,
        /*heading*/
        n[6]
      );
    },
    d(n) {
      n && Le(e);
    }
  };
}
function Hi(i) {
  let e, t;
  return {
    c() {
      e = Dt("p"), t = tt(
        /*paragraph*/
        i[5]
      ), Rt(e, "class", "svelte-1xg7h5n");
    },
    m(n, l) {
      Re(n, e, l), it(e, t);
    },
    p(n, l) {
      l & /*paragraph*/
      32 && It(
        t,
        /*paragraph*/
        n[5]
      );
    },
    d(n) {
      n && Le(e);
    }
  };
}
function Gs(i) {
  let e, t, n, l, o, r;
  const a = [Bs, qs], s = [];
  function f(m, w) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  n = f(i), l = s[n] = a[n](i);
  function c(m, w) {
    return (
      /*heading*/
      m[6] || /*paragraph*/
      m[5] ? js : Hs
    );
  }
  let _ = c(i), d = _(i);
  return {
    c() {
      e = Dt("div"), t = Dt("span"), l.c(), o = fn(), d.c(), Rt(t, "class", "icon-wrap svelte-1xg7h5n"), zi(
        t,
        "hovered",
        /*hovered*/
        i[4]
      ), Rt(e, "class", "wrap svelte-1xg7h5n");
    },
    m(m, w) {
      Re(m, e, w), it(e, t), s[n].m(t, null), it(e, o), d.m(e, null), r = !0;
    },
    p(m, [w]) {
      let E = n;
      n = f(m), n !== E && (Us(), en(s[E], 1, 1, () => {
        s[E] = null;
      }), Ps(), l = s[n], l || (l = s[n] = a[n](m), l.c()), $t(l, 1), l.m(t, null)), (!r || w & /*hovered*/
      16) && zi(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), _ === (_ = c(m)) && d ? d.p(m, w) : (d.d(1), d = _(m), d && (d.c(), d.m(e, null)));
    },
    i(m) {
      r || ($t(l), r = !0);
    },
    o(m) {
      en(l), r = !1;
    },
    d(m) {
      m && Le(e), s[n].d(), d.d();
    }
  };
}
function Ws(i, e, t) {
  let n, l, { type: o = "file" } = e, { i18n: r } = e, { message: a = void 0 } = e, { mode: s = "full" } = e, { hovered: f = !1 } = e, { placeholder: c = void 0 } = e;
  const _ = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return i.$$set = (d) => {
    "type" in d && t(0, o = d.type), "i18n" in d && t(1, r = d.i18n), "message" in d && t(2, a = d.message), "mode" in d && t(3, s = d.mode), "hovered" in d && t(4, f = d.hovered), "placeholder" in d && t(8, c = d.placeholder);
  }, i.$$.update = () => {
    i.$$.dirty & /*placeholder*/
    256 && t(6, [n, l] = c ? Ns(c) : [!1, !1], n, (t(5, l), t(8, c)));
  }, [o, r, a, s, f, l, n, _, c];
}
class Vs extends Ms {
  constructor(e) {
    super(), Fs(this, e, Ws, Gs, zs, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4,
      placeholder: 8
    });
  }
}
function gt(i) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; i > 1e3 && t < e.length - 1; )
    i /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(i) ? i : i.toFixed(1)) + n;
}
function Qt() {
}
const Ys = (i) => i;
function Xs(i, e) {
  return i != i ? e == e : i !== e || i && typeof i == "object" || typeof i == "function";
}
const Kl = typeof window < "u";
let ji = Kl ? () => window.performance.now() : () => Date.now(), Jl = Kl ? (i) => requestAnimationFrame(i) : Qt;
const pt = /* @__PURE__ */ new Set();
function Ql(i) {
  pt.forEach((e) => {
    e.c(i) || (pt.delete(e), e.f());
  }), pt.size !== 0 && Jl(Ql);
}
function Zs(i) {
  let e;
  return pt.size === 0 && Jl(Ql), {
    promise: new Promise((t) => {
      pt.add(e = { c: i, f: t });
    }),
    abort() {
      pt.delete(e);
    }
  };
}
function Ks(i, { delay: e = 0, duration: t = 400, easing: n = Ys } = {}) {
  const l = +getComputedStyle(i).opacity;
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (o) => `opacity: ${o * l}`
  };
}
const mt = [];
function Js(i, e = Qt) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function l(a) {
    if (Xs(i, a) && (i = a, t)) {
      const s = !mt.length;
      for (const f of n)
        f[1](), mt.push(f, i);
      if (s) {
        for (let f = 0; f < mt.length; f += 2)
          mt[f][0](mt[f + 1]);
        mt.length = 0;
      }
    }
  }
  function o(a) {
    l(a(i));
  }
  function r(a, s = Qt) {
    const f = [a, s];
    return n.add(f), n.size === 1 && (t = e(l, o) || Qt), a(i), () => {
      n.delete(f), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: l, update: o, subscribe: r };
}
function Gi(i) {
  return Object.prototype.toString.call(i) === "[object Date]";
}
function Hn(i, e, t, n) {
  if (typeof t == "number" || Gi(t)) {
    const l = n - t, o = (t - e) / (i.dt || 1 / 60), r = i.opts.stiffness * l, a = i.opts.damping * o, s = (r - a) * i.inv_mass, f = (o + s) * i.dt;
    return Math.abs(f) < i.opts.precision && Math.abs(l) < i.opts.precision ? n : (i.settled = !1, Gi(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (l, o) => Hn(i, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const l = {};
      for (const o in t)
        l[o] = Hn(i, e[o], t[o], n[o]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Wi(i, e = {}) {
  const t = Js(i), { stiffness: n = 0.15, damping: l = 0.8, precision: o = 0.01 } = e;
  let r, a, s, f = i, c = i, _ = 1, d = 0, m = !1;
  function w(k, p = {}) {
    c = k;
    const L = s = {};
    return i == null || p.hard || E.stiffness >= 1 && E.damping >= 1 ? (m = !0, r = ji(), f = k, t.set(i = c), Promise.resolve()) : (p.soft && (d = 1 / ((p.soft === !0 ? 0.5 : +p.soft) * 60), _ = 0), a || (r = ji(), m = !1, a = Zs((b) => {
      if (m)
        return m = !1, a = null, !1;
      _ = Math.min(_ + d, 1);
      const h = {
        inv_mass: _,
        opts: E,
        settled: !0,
        dt: (b - r) * 60 / 1e3
      }, N = Hn(h, f, i, c);
      return r = b, f = i, t.set(i = N), h.settled && (a = null), !h.settled;
    })), new Promise((b) => {
      a.promise.then(() => {
        L === s && b();
      });
    }));
  }
  const E = {
    set: w,
    update: (k, p) => w(k(c, i), p),
    subscribe: t.subscribe,
    stiffness: n,
    damping: l,
    precision: o
  };
  return E;
}
const {
  SvelteComponent: Qs,
  append: Te,
  attr: O,
  component_subscribe: Vi,
  detach: xs,
  element: $s,
  init: ea,
  insert: ta,
  noop: Yi,
  safe_not_equal: na,
  set_style: Wt,
  svg_element: ye,
  toggle_class: Xi
} = window.__gradio__svelte__internal, { onMount: ia } = window.__gradio__svelte__internal;
function la(i) {
  let e, t, n, l, o, r, a, s, f, c, _, d;
  return {
    c() {
      e = $s("div"), t = ye("svg"), n = ye("g"), l = ye("path"), o = ye("path"), r = ye("path"), a = ye("path"), s = ye("g"), f = ye("path"), c = ye("path"), _ = ye("path"), d = ye("path"), O(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), O(l, "fill", "#FF7C00"), O(l, "fill-opacity", "0.4"), O(l, "class", "svelte-43sxxs"), O(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), O(o, "fill", "#FF7C00"), O(o, "class", "svelte-43sxxs"), O(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), O(r, "fill", "#FF7C00"), O(r, "fill-opacity", "0.4"), O(r, "class", "svelte-43sxxs"), O(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), O(a, "fill", "#FF7C00"), O(a, "class", "svelte-43sxxs"), Wt(n, "transform", "translate(" + /*$top*/
      i[1][0] + "px, " + /*$top*/
      i[1][1] + "px)"), O(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), O(f, "fill", "#FF7C00"), O(f, "fill-opacity", "0.4"), O(f, "class", "svelte-43sxxs"), O(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), O(c, "fill", "#FF7C00"), O(c, "class", "svelte-43sxxs"), O(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), O(_, "fill", "#FF7C00"), O(_, "fill-opacity", "0.4"), O(_, "class", "svelte-43sxxs"), O(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), O(d, "fill", "#FF7C00"), O(d, "class", "svelte-43sxxs"), Wt(s, "transform", "translate(" + /*$bottom*/
      i[2][0] + "px, " + /*$bottom*/
      i[2][1] + "px)"), O(t, "viewBox", "-1200 -1200 3000 3000"), O(t, "fill", "none"), O(t, "xmlns", "http://www.w3.org/2000/svg"), O(t, "class", "svelte-43sxxs"), O(e, "class", "svelte-43sxxs"), Xi(
        e,
        "margin",
        /*margin*/
        i[0]
      );
    },
    m(m, w) {
      ta(m, e, w), Te(e, t), Te(t, n), Te(n, l), Te(n, o), Te(n, r), Te(n, a), Te(t, s), Te(s, f), Te(s, c), Te(s, _), Te(s, d);
    },
    p(m, [w]) {
      w & /*$top*/
      2 && Wt(n, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), w & /*$bottom*/
      4 && Wt(s, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), w & /*margin*/
      1 && Xi(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Yi,
    o: Yi,
    d(m) {
      m && xs(e);
    }
  };
}
function oa(i, e, t) {
  let n, l;
  var o = this && this.__awaiter || function(m, w, E, k) {
    function p(L) {
      return L instanceof E ? L : new E(function(b) {
        b(L);
      });
    }
    return new (E || (E = Promise))(function(L, b) {
      function h(H) {
        try {
          M(k.next(H));
        } catch (j) {
          b(j);
        }
      }
      function N(H) {
        try {
          M(k.throw(H));
        } catch (j) {
          b(j);
        }
      }
      function M(H) {
        H.done ? L(H.value) : p(H.value).then(h, N);
      }
      M((k = k.apply(m, w || [])).next());
    });
  };
  let { margin: r = !0 } = e;
  const a = Wi([0, 0]);
  Vi(i, a, (m) => t(1, n = m));
  const s = Wi([0, 0]);
  Vi(i, s, (m) => t(2, l = m));
  let f;
  function c() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 140]), s.set([-125, -140])]), yield Promise.all([a.set([-125, 140]), s.set([125, -140])]), yield Promise.all([a.set([-125, 0]), s.set([125, -0])]), yield Promise.all([a.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function _() {
    return o(this, void 0, void 0, function* () {
      yield c(), f || _();
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 0]), s.set([-125, 0])]), _();
    });
  }
  return ia(() => (d(), () => f = !0)), i.$$set = (m) => {
    "margin" in m && t(0, r = m.margin);
  }, [r, n, l, a, s];
}
class ra extends Qs {
  constructor(e) {
    super(), ea(this, e, oa, la, na, { margin: 0 });
  }
}
const {
  SvelteComponent: sa,
  append: nt,
  attr: Ce,
  binding_callbacks: Zi,
  check_outros: jn,
  create_component: xl,
  create_slot: $l,
  destroy_component: eo,
  destroy_each: to,
  detach: R,
  element: Fe,
  empty: bt,
  ensure_array_like: tn,
  get_all_dirty_from_scope: no,
  get_slot_changes: io,
  group_outros: Gn,
  init: aa,
  insert: D,
  mount_component: lo,
  noop: Wn,
  safe_not_equal: fa,
  set_data: pe,
  set_style: Ke,
  space: ge,
  text: q,
  toggle_class: he,
  transition_in: Se,
  transition_out: ze,
  update_slot_base: oo
} = window.__gradio__svelte__internal, { tick: ca } = window.__gradio__svelte__internal, { onDestroy: ua } = window.__gradio__svelte__internal, { createEventDispatcher: _a } = window.__gradio__svelte__internal, da = (i) => ({}), Ki = (i) => ({}), ma = (i) => ({}), Ji = (i) => ({});
function Qi(i, e, t) {
  const n = i.slice();
  return n[41] = e[t], n[43] = t, n;
}
function xi(i, e, t) {
  const n = i.slice();
  return n[41] = e[t], n;
}
function ha(i) {
  let e, t, n, l, o = (
    /*i18n*/
    i[1]("common.error") + ""
  ), r, a, s;
  t = new pr({
    props: {
      Icon: Or,
      label: (
        /*i18n*/
        i[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    i[32]
  );
  const f = (
    /*#slots*/
    i[30].error
  ), c = $l(
    f,
    i,
    /*$$scope*/
    i[29],
    Ki
  );
  return {
    c() {
      e = Fe("div"), xl(t.$$.fragment), n = ge(), l = Fe("span"), r = q(o), a = ge(), c && c.c(), Ce(e, "class", "clear-status svelte-17v219f"), Ce(l, "class", "error svelte-17v219f");
    },
    m(_, d) {
      D(_, e, d), lo(t, e, null), D(_, n, d), D(_, l, d), nt(l, r), D(_, a, d), c && c.m(_, d), s = !0;
    },
    p(_, d) {
      const m = {};
      d[0] & /*i18n*/
      2 && (m.label = /*i18n*/
      _[1]("common.clear")), t.$set(m), (!s || d[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      _[1]("common.error") + "") && pe(r, o), c && c.p && (!s || d[0] & /*$$scope*/
      536870912) && oo(
        c,
        f,
        _,
        /*$$scope*/
        _[29],
        s ? io(
          f,
          /*$$scope*/
          _[29],
          d,
          da
        ) : no(
          /*$$scope*/
          _[29]
        ),
        Ki
      );
    },
    i(_) {
      s || (Se(t.$$.fragment, _), Se(c, _), s = !0);
    },
    o(_) {
      ze(t.$$.fragment, _), ze(c, _), s = !1;
    },
    d(_) {
      _ && (R(e), R(n), R(l), R(a)), eo(t), c && c.d(_);
    }
  };
}
function ga(i) {
  let e, t, n, l, o, r, a, s, f, c = (
    /*variant*/
    i[8] === "default" && /*show_eta_bar*/
    i[18] && /*show_progress*/
    i[6] === "full" && $i(i)
  );
  function _(b, h) {
    if (
      /*progress*/
      b[7]
    ) return wa;
    if (
      /*queue_position*/
      b[2] !== null && /*queue_size*/
      b[3] !== void 0 && /*queue_position*/
      b[2] >= 0
    ) return ba;
    if (
      /*queue_position*/
      b[2] === 0
    ) return pa;
  }
  let d = _(i), m = d && d(i), w = (
    /*timer*/
    i[5] && nl(i)
  );
  const E = [Ta, Ea], k = [];
  function p(b, h) {
    return (
      /*last_progress_level*/
      b[15] != null ? 0 : (
        /*show_progress*/
        b[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = p(i)) && (r = k[o] = E[o](i));
  let L = !/*timer*/
  i[5] && fl(i);
  return {
    c() {
      c && c.c(), e = ge(), t = Fe("div"), m && m.c(), n = ge(), w && w.c(), l = ge(), r && r.c(), a = ge(), L && L.c(), s = bt(), Ce(t, "class", "progress-text svelte-17v219f"), he(
        t,
        "meta-text-center",
        /*variant*/
        i[8] === "center"
      ), he(
        t,
        "meta-text",
        /*variant*/
        i[8] === "default"
      );
    },
    m(b, h) {
      c && c.m(b, h), D(b, e, h), D(b, t, h), m && m.m(t, null), nt(t, n), w && w.m(t, null), D(b, l, h), ~o && k[o].m(b, h), D(b, a, h), L && L.m(b, h), D(b, s, h), f = !0;
    },
    p(b, h) {
      /*variant*/
      b[8] === "default" && /*show_eta_bar*/
      b[18] && /*show_progress*/
      b[6] === "full" ? c ? c.p(b, h) : (c = $i(b), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), d === (d = _(b)) && m ? m.p(b, h) : (m && m.d(1), m = d && d(b), m && (m.c(), m.m(t, n))), /*timer*/
      b[5] ? w ? w.p(b, h) : (w = nl(b), w.c(), w.m(t, null)) : w && (w.d(1), w = null), (!f || h[0] & /*variant*/
      256) && he(
        t,
        "meta-text-center",
        /*variant*/
        b[8] === "center"
      ), (!f || h[0] & /*variant*/
      256) && he(
        t,
        "meta-text",
        /*variant*/
        b[8] === "default"
      );
      let N = o;
      o = p(b), o === N ? ~o && k[o].p(b, h) : (r && (Gn(), ze(k[N], 1, 1, () => {
        k[N] = null;
      }), jn()), ~o ? (r = k[o], r ? r.p(b, h) : (r = k[o] = E[o](b), r.c()), Se(r, 1), r.m(a.parentNode, a)) : r = null), /*timer*/
      b[5] ? L && (Gn(), ze(L, 1, 1, () => {
        L = null;
      }), jn()) : L ? (L.p(b, h), h[0] & /*timer*/
      32 && Se(L, 1)) : (L = fl(b), L.c(), Se(L, 1), L.m(s.parentNode, s));
    },
    i(b) {
      f || (Se(r), Se(L), f = !0);
    },
    o(b) {
      ze(r), ze(L), f = !1;
    },
    d(b) {
      b && (R(e), R(t), R(l), R(a), R(s)), c && c.d(b), m && m.d(), w && w.d(), ~o && k[o].d(b), L && L.d(b);
    }
  };
}
function $i(i) {
  let e, t = `translateX(${/*eta_level*/
  (i[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Fe("div"), Ce(e, "class", "eta-bar svelte-17v219f"), Ke(e, "transform", t);
    },
    m(n, l) {
      D(n, e, l);
    },
    p(n, l) {
      l[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Ke(e, "transform", t);
    },
    d(n) {
      n && R(e);
    }
  };
}
function pa(i) {
  let e;
  return {
    c() {
      e = q("processing |");
    },
    m(t, n) {
      D(t, e, n);
    },
    p: Wn,
    d(t) {
      t && R(e);
    }
  };
}
function ba(i) {
  let e, t = (
    /*queue_position*/
    i[2] + 1 + ""
  ), n, l, o, r;
  return {
    c() {
      e = q("queue: "), n = q(t), l = q("/"), o = q(
        /*queue_size*/
        i[3]
      ), r = q(" |");
    },
    m(a, s) {
      D(a, e, s), D(a, n, s), D(a, l, s), D(a, o, s), D(a, r, s);
    },
    p(a, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      a[2] + 1 + "") && pe(n, t), s[0] & /*queue_size*/
      8 && pe(
        o,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (R(e), R(n), R(l), R(o), R(r));
    }
  };
}
function wa(i) {
  let e, t = tn(
    /*progress*/
    i[7]
  ), n = [];
  for (let l = 0; l < t.length; l += 1)
    n[l] = tl(xi(i, t, l));
  return {
    c() {
      for (let l = 0; l < n.length; l += 1)
        n[l].c();
      e = bt();
    },
    m(l, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(l, o);
      D(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress*/
      128) {
        t = tn(
          /*progress*/
          l[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const a = xi(l, t, r);
          n[r] ? n[r].p(a, o) : (n[r] = tl(a), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(l) {
      l && R(e), to(n, l);
    }
  };
}
function el(i) {
  let e, t = (
    /*p*/
    i[41].unit + ""
  ), n, l, o = " ", r;
  function a(c, _) {
    return (
      /*p*/
      c[41].length != null ? ka : va
    );
  }
  let s = a(i), f = s(i);
  return {
    c() {
      f.c(), e = ge(), n = q(t), l = q(" | "), r = q(o);
    },
    m(c, _) {
      f.m(c, _), D(c, e, _), D(c, n, _), D(c, l, _), D(c, r, _);
    },
    p(c, _) {
      s === (s = a(c)) && f ? f.p(c, _) : (f.d(1), f = s(c), f && (f.c(), f.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[41].unit + "") && pe(n, t);
    },
    d(c) {
      c && (R(e), R(n), R(l), R(r)), f.d(c);
    }
  };
}
function va(i) {
  let e = gt(
    /*p*/
    i[41].index || 0
  ) + "", t;
  return {
    c() {
      t = q(e);
    },
    m(n, l) {
      D(n, t, l);
    },
    p(n, l) {
      l[0] & /*progress*/
      128 && e !== (e = gt(
        /*p*/
        n[41].index || 0
      ) + "") && pe(t, e);
    },
    d(n) {
      n && R(t);
    }
  };
}
function ka(i) {
  let e = gt(
    /*p*/
    i[41].index || 0
  ) + "", t, n, l = gt(
    /*p*/
    i[41].length
  ) + "", o;
  return {
    c() {
      t = q(e), n = q("/"), o = q(l);
    },
    m(r, a) {
      D(r, t, a), D(r, n, a), D(r, o, a);
    },
    p(r, a) {
      a[0] & /*progress*/
      128 && e !== (e = gt(
        /*p*/
        r[41].index || 0
      ) + "") && pe(t, e), a[0] & /*progress*/
      128 && l !== (l = gt(
        /*p*/
        r[41].length
      ) + "") && pe(o, l);
    },
    d(r) {
      r && (R(t), R(n), R(o));
    }
  };
}
function tl(i) {
  let e, t = (
    /*p*/
    i[41].index != null && el(i)
  );
  return {
    c() {
      t && t.c(), e = bt();
    },
    m(n, l) {
      t && t.m(n, l), D(n, e, l);
    },
    p(n, l) {
      /*p*/
      n[41].index != null ? t ? t.p(n, l) : (t = el(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && R(e), t && t.d(n);
    }
  };
}
function nl(i) {
  let e, t = (
    /*eta*/
    i[0] ? `/${/*formatted_eta*/
    i[19]}` : ""
  ), n, l;
  return {
    c() {
      e = q(
        /*formatted_timer*/
        i[20]
      ), n = q(t), l = q("s");
    },
    m(o, r) {
      D(o, e, r), D(o, n, r), D(o, l, r);
    },
    p(o, r) {
      r[0] & /*formatted_timer*/
      1048576 && pe(
        e,
        /*formatted_timer*/
        o[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && pe(n, t);
    },
    d(o) {
      o && (R(e), R(n), R(l));
    }
  };
}
function Ea(i) {
  let e, t;
  return e = new ra({
    props: { margin: (
      /*variant*/
      i[8] === "default"
    ) }
  }), {
    c() {
      xl(e.$$.fragment);
    },
    m(n, l) {
      lo(e, n, l), t = !0;
    },
    p(n, l) {
      const o = {};
      l[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (Se(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ze(e.$$.fragment, n), t = !1;
    },
    d(n) {
      eo(e, n);
    }
  };
}
function Ta(i) {
  let e, t, n, l, o, r = `${/*last_progress_level*/
  i[15] * 100}%`, a = (
    /*progress*/
    i[7] != null && il(i)
  );
  return {
    c() {
      e = Fe("div"), t = Fe("div"), a && a.c(), n = ge(), l = Fe("div"), o = Fe("div"), Ce(t, "class", "progress-level-inner svelte-17v219f"), Ce(o, "class", "progress-bar svelte-17v219f"), Ke(o, "width", r), Ce(l, "class", "progress-bar-wrap svelte-17v219f"), Ce(e, "class", "progress-level svelte-17v219f");
    },
    m(s, f) {
      D(s, e, f), nt(e, t), a && a.m(t, null), nt(e, n), nt(e, l), nt(l, o), i[31](o);
    },
    p(s, f) {
      /*progress*/
      s[7] != null ? a ? a.p(s, f) : (a = il(s), a.c(), a.m(t, null)) : a && (a.d(1), a = null), f[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      s[15] * 100}%`) && Ke(o, "width", r);
    },
    i: Wn,
    o: Wn,
    d(s) {
      s && R(e), a && a.d(), i[31](null);
    }
  };
}
function il(i) {
  let e, t = tn(
    /*progress*/
    i[7]
  ), n = [];
  for (let l = 0; l < t.length; l += 1)
    n[l] = al(Qi(i, t, l));
  return {
    c() {
      for (let l = 0; l < n.length; l += 1)
        n[l].c();
      e = bt();
    },
    m(l, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(l, o);
      D(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = tn(
          /*progress*/
          l[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const a = Qi(l, t, r);
          n[r] ? n[r].p(a, o) : (n[r] = al(a), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(l) {
      l && R(e), to(n, l);
    }
  };
}
function ll(i) {
  let e, t, n, l, o = (
    /*i*/
    i[43] !== 0 && ya()
  ), r = (
    /*p*/
    i[41].desc != null && ol(i)
  ), a = (
    /*p*/
    i[41].desc != null && /*progress_level*/
    i[14] && /*progress_level*/
    i[14][
      /*i*/
      i[43]
    ] != null && rl()
  ), s = (
    /*progress_level*/
    i[14] != null && sl(i)
  );
  return {
    c() {
      o && o.c(), e = ge(), r && r.c(), t = ge(), a && a.c(), n = ge(), s && s.c(), l = bt();
    },
    m(f, c) {
      o && o.m(f, c), D(f, e, c), r && r.m(f, c), D(f, t, c), a && a.m(f, c), D(f, n, c), s && s.m(f, c), D(f, l, c);
    },
    p(f, c) {
      /*p*/
      f[41].desc != null ? r ? r.p(f, c) : (r = ol(f), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), /*p*/
      f[41].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[43]
      ] != null ? a || (a = rl(), a.c(), a.m(n.parentNode, n)) : a && (a.d(1), a = null), /*progress_level*/
      f[14] != null ? s ? s.p(f, c) : (s = sl(f), s.c(), s.m(l.parentNode, l)) : s && (s.d(1), s = null);
    },
    d(f) {
      f && (R(e), R(t), R(n), R(l)), o && o.d(f), r && r.d(f), a && a.d(f), s && s.d(f);
    }
  };
}
function ya(i) {
  let e;
  return {
    c() {
      e = q(" /");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && R(e);
    }
  };
}
function ol(i) {
  let e = (
    /*p*/
    i[41].desc + ""
  ), t;
  return {
    c() {
      t = q(e);
    },
    m(n, l) {
      D(n, t, l);
    },
    p(n, l) {
      l[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && pe(t, e);
    },
    d(n) {
      n && R(t);
    }
  };
}
function rl(i) {
  let e;
  return {
    c() {
      e = q("-");
    },
    m(t, n) {
      D(t, e, n);
    },
    d(t) {
      t && R(e);
    }
  };
}
function sl(i) {
  let e = (100 * /*progress_level*/
  (i[14][
    /*i*/
    i[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = q(e), n = q("%");
    },
    m(l, o) {
      D(l, t, o), D(l, n, o);
    },
    p(l, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[43]
      ] || 0)).toFixed(1) + "") && pe(t, e);
    },
    d(l) {
      l && (R(t), R(n));
    }
  };
}
function al(i) {
  let e, t = (
    /*p*/
    (i[41].desc != null || /*progress_level*/
    i[14] && /*progress_level*/
    i[14][
      /*i*/
      i[43]
    ] != null) && ll(i)
  );
  return {
    c() {
      t && t.c(), e = bt();
    },
    m(n, l) {
      t && t.m(n, l), D(n, e, l);
    },
    p(n, l) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, l) : (t = ll(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && R(e), t && t.d(n);
    }
  };
}
function fl(i) {
  let e, t, n, l;
  const o = (
    /*#slots*/
    i[30]["additional-loading-text"]
  ), r = $l(
    o,
    i,
    /*$$scope*/
    i[29],
    Ji
  );
  return {
    c() {
      e = Fe("p"), t = q(
        /*loading_text*/
        i[9]
      ), n = ge(), r && r.c(), Ce(e, "class", "loading svelte-17v219f");
    },
    m(a, s) {
      D(a, e, s), nt(e, t), D(a, n, s), r && r.m(a, s), l = !0;
    },
    p(a, s) {
      (!l || s[0] & /*loading_text*/
      512) && pe(
        t,
        /*loading_text*/
        a[9]
      ), r && r.p && (!l || s[0] & /*$$scope*/
      536870912) && oo(
        r,
        o,
        a,
        /*$$scope*/
        a[29],
        l ? io(
          o,
          /*$$scope*/
          a[29],
          s,
          ma
        ) : no(
          /*$$scope*/
          a[29]
        ),
        Ji
      );
    },
    i(a) {
      l || (Se(r, a), l = !0);
    },
    o(a) {
      ze(r, a), l = !1;
    },
    d(a) {
      a && (R(e), R(n)), r && r.d(a);
    }
  };
}
function Aa(i) {
  let e, t, n, l, o;
  const r = [ga, ha], a = [];
  function s(f, c) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(i)) && (n = a[t] = r[t](i)), {
    c() {
      e = Fe("div"), n && n.c(), Ce(e, "class", l = "wrap " + /*variant*/
      i[8] + " " + /*show_progress*/
      i[6] + " svelte-17v219f"), he(e, "hide", !/*status*/
      i[4] || /*status*/
      i[4] === "complete" || /*show_progress*/
      i[6] === "hidden" || /*status*/
      i[4] == "streaming"), he(
        e,
        "translucent",
        /*variant*/
        i[8] === "center" && /*status*/
        (i[4] === "pending" || /*status*/
        i[4] === "error") || /*translucent*/
        i[11] || /*show_progress*/
        i[6] === "minimal"
      ), he(
        e,
        "generating",
        /*status*/
        i[4] === "generating" && /*show_progress*/
        i[6] === "full"
      ), he(
        e,
        "border",
        /*border*/
        i[12]
      ), Ke(
        e,
        "position",
        /*absolute*/
        i[10] ? "absolute" : "static"
      ), Ke(
        e,
        "padding",
        /*absolute*/
        i[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, c) {
      D(f, e, c), ~t && a[t].m(e, null), i[33](e), o = !0;
    },
    p(f, c) {
      let _ = t;
      t = s(f), t === _ ? ~t && a[t].p(f, c) : (n && (Gn(), ze(a[_], 1, 1, () => {
        a[_] = null;
      }), jn()), ~t ? (n = a[t], n ? n.p(f, c) : (n = a[t] = r[t](f), n.c()), Se(n, 1), n.m(e, null)) : n = null), (!o || c[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-17v219f")) && Ce(e, "class", l), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && he(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden" || /*status*/
      f[4] == "streaming"), (!o || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && he(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!o || c[0] & /*variant, show_progress, status, show_progress*/
      336) && he(
        e,
        "generating",
        /*status*/
        f[4] === "generating" && /*show_progress*/
        f[6] === "full"
      ), (!o || c[0] & /*variant, show_progress, border*/
      4416) && he(
        e,
        "border",
        /*border*/
        f[12]
      ), c[0] & /*absolute*/
      1024 && Ke(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && Ke(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      o || (Se(n), o = !0);
    },
    o(f) {
      ze(n), o = !1;
    },
    d(f) {
      f && R(e), ~t && a[t].d(), i[33](null);
    }
  };
}
var Sa = function(i, e, t, n) {
  function l(o) {
    return o instanceof t ? o : new t(function(r) {
      r(o);
    });
  }
  return new (t || (t = Promise))(function(o, r) {
    function a(c) {
      try {
        f(n.next(c));
      } catch (_) {
        r(_);
      }
    }
    function s(c) {
      try {
        f(n.throw(c));
      } catch (_) {
        r(_);
      }
    }
    function f(c) {
      c.done ? o(c.value) : l(c.value).then(a, s);
    }
    f((n = n.apply(i, e || [])).next());
  });
};
let Vt = [], Rn = !1;
const Ca = typeof window < "u", ro = Ca ? window.requestAnimationFrame : (i) => {
};
function La(i) {
  return Sa(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Vt.push(e), !Rn) Rn = !0;
      else return;
      yield ca(), ro(() => {
        let n = [0, 0];
        for (let l = 0; l < Vt.length; l++) {
          const r = Vt[l].getBoundingClientRect();
          (l === 0 || r.top + window.scrollY <= n[0]) && (n[0] = r.top + window.scrollY, n[1] = l);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Rn = !1, Vt = [];
      });
    }
  });
}
function Ra(i, e, t) {
  let n, { $$slots: l = {}, $$scope: o } = e;
  this && this.__awaiter;
  const r = _a();
  let { i18n: a } = e, { eta: s = null } = e, { queue_position: f } = e, { queue_size: c } = e, { status: _ } = e, { scroll_to_output: d = !1 } = e, { timer: m = !0 } = e, { show_progress: w = "full" } = e, { message: E = null } = e, { progress: k = null } = e, { variant: p = "default" } = e, { loading_text: L = "Loading..." } = e, { absolute: b = !0 } = e, { translucent: h = !1 } = e, { border: N = !1 } = e, { autoscroll: M } = e, H, j = !1, S = 0, ce = 0, G = null, re = null, De = 0, C = null, V, P = null, y = !0;
  const Ge = () => {
    t(0, s = t(27, G = t(19, F = null))), t(25, S = performance.now()), t(26, ce = 0), j = !0, Ie();
  };
  function Ie() {
    ro(() => {
      t(26, ce = (performance.now() - S) / 1e3), j && Ie();
    });
  }
  function Oe() {
    t(26, ce = 0), t(0, s = t(27, G = t(19, F = null))), j && (j = !1);
  }
  ua(() => {
    j && Oe();
  });
  let F = null;
  function st(v) {
    Zi[v ? "unshift" : "push"](() => {
      P = v, t(16, P), t(7, k), t(14, C), t(15, V);
    });
  }
  const z = () => {
    r("clear_status");
  };
  function me(v) {
    Zi[v ? "unshift" : "push"](() => {
      H = v, t(13, H);
    });
  }
  return i.$$set = (v) => {
    "i18n" in v && t(1, a = v.i18n), "eta" in v && t(0, s = v.eta), "queue_position" in v && t(2, f = v.queue_position), "queue_size" in v && t(3, c = v.queue_size), "status" in v && t(4, _ = v.status), "scroll_to_output" in v && t(22, d = v.scroll_to_output), "timer" in v && t(5, m = v.timer), "show_progress" in v && t(6, w = v.show_progress), "message" in v && t(23, E = v.message), "progress" in v && t(7, k = v.progress), "variant" in v && t(8, p = v.variant), "loading_text" in v && t(9, L = v.loading_text), "absolute" in v && t(10, b = v.absolute), "translucent" in v && t(11, h = v.translucent), "border" in v && t(12, N = v.border), "autoscroll" in v && t(24, M = v.autoscroll), "$$scope" in v && t(29, o = v.$$scope);
  }, i.$$.update = () => {
    i.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = G), s != null && G !== s && (t(28, re = (performance.now() - S) / 1e3 + s), t(19, F = re.toFixed(1)), t(27, G = s))), i.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, De = re === null || re <= 0 || !ce ? null : Math.min(ce / re, 1)), i.$$.dirty[0] & /*progress*/
    128 && k != null && t(18, y = !1), i.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (k != null ? t(14, C = k.map((v) => {
      if (v.index != null && v.length != null)
        return v.index / v.length;
      if (v.progress != null)
        return v.progress;
    })) : t(14, C = null), C ? (t(15, V = C[C.length - 1]), P && (V === 0 ? t(16, P.style.transition = "0", P) : t(16, P.style.transition = "150ms", P))) : t(15, V = void 0)), i.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? Ge() : Oe()), i.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && H && d && (_ === "pending" || _ === "complete") && La(H, M), i.$$.dirty[0] & /*status, message*/
    8388624, i.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = ce.toFixed(1));
  }, [
    s,
    a,
    f,
    c,
    _,
    m,
    w,
    k,
    p,
    L,
    b,
    h,
    N,
    H,
    C,
    V,
    P,
    De,
    y,
    F,
    n,
    r,
    d,
    E,
    M,
    S,
    ce,
    G,
    re,
    o,
    l,
    st,
    z,
    me
  ];
}
class Da extends sa {
  constructor(e) {
    super(), aa(
      this,
      e,
      Ra,
      Aa,
      fa,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.1.6 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.1.6/LICENSE */
const {
  entries: so,
  setPrototypeOf: cl,
  isFrozen: Ia,
  getPrototypeOf: Oa,
  getOwnPropertyDescriptor: Na
} = Object;
let {
  freeze: oe,
  seal: be,
  create: ao
} = Object, {
  apply: Vn,
  construct: Yn
} = typeof Reflect < "u" && Reflect;
oe || (oe = function(e) {
  return e;
});
be || (be = function(e) {
  return e;
});
Vn || (Vn = function(e, t, n) {
  return e.apply(t, n);
});
Yn || (Yn = function(e, t) {
  return new e(...t);
});
const Yt = de(Array.prototype.forEach), ul = de(Array.prototype.pop), yt = de(Array.prototype.push), xt = de(String.prototype.toLowerCase), Dn = de(String.prototype.toString), _l = de(String.prototype.match), At = de(String.prototype.replace), Ma = de(String.prototype.indexOf), Pa = de(String.prototype.trim), Ae = de(Object.prototype.hasOwnProperty), ie = de(RegExp.prototype.test), St = Ua(TypeError);
function de(i) {
  return function(e) {
    for (var t = arguments.length, n = new Array(t > 1 ? t - 1 : 0), l = 1; l < t; l++)
      n[l - 1] = arguments[l];
    return Vn(i, e, n);
  };
}
function Ua(i) {
  return function() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
      t[n] = arguments[n];
    return Yn(i, t);
  };
}
function I(i, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : xt;
  cl && cl(i, null);
  let n = e.length;
  for (; n--; ) {
    let l = e[n];
    if (typeof l == "string") {
      const o = t(l);
      o !== l && (Ia(e) || (e[n] = o), l = o);
    }
    i[l] = !0;
  }
  return i;
}
function Fa(i) {
  for (let e = 0; e < i.length; e++)
    Ae(i, e) || (i[e] = null);
  return i;
}
function et(i) {
  const e = ao(null);
  for (const [t, n] of so(i))
    Ae(i, t) && (Array.isArray(n) ? e[t] = Fa(n) : n && typeof n == "object" && n.constructor === Object ? e[t] = et(n) : e[t] = n);
  return e;
}
function Ct(i, e) {
  for (; i !== null; ) {
    const n = Na(i, e);
    if (n) {
      if (n.get)
        return de(n.get);
      if (typeof n.value == "function")
        return de(n.value);
    }
    i = Oa(i);
  }
  function t() {
    return null;
  }
  return t;
}
const dl = oe(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), In = oe(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), On = oe(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), za = oe(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), Nn = oe(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), qa = oe(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), ml = oe(["#text"]), hl = oe(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), Mn = oe(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), gl = oe(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Xt = oe(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), Ba = be(/\{\{[\w\W]*|[\w\W]*\}\}/gm), Ha = be(/<%[\w\W]*|[\w\W]*%>/gm), ja = be(/\${[\w\W]*}/gm), Ga = be(/^data-[\-\w.\u00B7-\uFFFF]/), Wa = be(/^aria-[\-\w]+$/), fo = be(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), Va = be(/^(?:\w+script|data):/i), Ya = be(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), co = be(/^html$/i), Xa = be(/^[a-z][.\w]*(-[.\w]+)+$/i);
var pl = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR: Ba,
  ERB_EXPR: Ha,
  TMPLIT_EXPR: ja,
  DATA_ATTR: Ga,
  ARIA_ATTR: Wa,
  IS_ALLOWED_URI: fo,
  IS_SCRIPT_OR_DATA: Va,
  ATTR_WHITESPACE: Ya,
  DOCTYPE_NAME: co,
  CUSTOM_ELEMENT: Xa
});
const Lt = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, Za = function() {
  return typeof window > "u" ? null : window;
}, Ka = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let n = null;
  const l = "data-tt-policy-suffix";
  t && t.hasAttribute(l) && (n = t.getAttribute(l));
  const o = "dompurify" + (n ? "#" + n : "");
  try {
    return e.createPolicy(o, {
      createHTML(r) {
        return r;
      },
      createScriptURL(r) {
        return r;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function uo() {
  let i = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Za();
  const e = (A) => uo(A);
  if (e.version = "3.1.6", e.removed = [], !i || !i.document || i.document.nodeType !== Lt.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = i;
  const n = t, l = n.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: r,
    Node: a,
    Element: s,
    NodeFilter: f,
    NamedNodeMap: c = i.NamedNodeMap || i.MozNamedAttrMap,
    HTMLFormElement: _,
    DOMParser: d,
    trustedTypes: m
  } = i, w = s.prototype, E = Ct(w, "cloneNode"), k = Ct(w, "remove"), p = Ct(w, "nextSibling"), L = Ct(w, "childNodes"), b = Ct(w, "parentNode");
  if (typeof r == "function") {
    const A = t.createElement("template");
    A.content && A.content.ownerDocument && (t = A.content.ownerDocument);
  }
  let h, N = "";
  const {
    implementation: M,
    createNodeIterator: H,
    createDocumentFragment: j,
    getElementsByTagName: S
  } = t, {
    importNode: ce
  } = n;
  let G = {};
  e.isSupported = typeof so == "function" && typeof b == "function" && M && M.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: re,
    ERB_EXPR: De,
    TMPLIT_EXPR: C,
    DATA_ATTR: V,
    ARIA_ATTR: P,
    IS_SCRIPT_OR_DATA: y,
    ATTR_WHITESPACE: Ge,
    CUSTOM_ELEMENT: Ie
  } = pl;
  let {
    IS_ALLOWED_URI: Oe
  } = pl, F = null;
  const st = I({}, [...dl, ...In, ...On, ...Nn, ...ml]);
  let z = null;
  const me = I({}, [...hl, ...Mn, ...gl, ...Xt]);
  let v = Object.seal(ao(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), Je = null, We = null, Qe = !0, wt = !0, Ve = !1, xe = !0, Ye = !1, vt = !0, we = !1, ve = !1, $e = !1, at = !1, Mt = !1, Pt = !1, $n = !0, ei = !1;
  const wo = "user-content-";
  let cn = !0, kt = !1, ft = {}, ct = null;
  const ti = I({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let ni = null;
  const ii = I({}, ["audio", "video", "img", "source", "image", "track"]);
  let un = null;
  const li = I({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), Ut = "http://www.w3.org/1998/Math/MathML", Ft = "http://www.w3.org/2000/svg", qe = "http://www.w3.org/1999/xhtml";
  let ut = qe, _n = !1, dn = null;
  const vo = I({}, [Ut, Ft, qe], Dn);
  let Et = null;
  const ko = ["application/xhtml+xml", "text/html"], Eo = "text/html";
  let Y = null, _t = null;
  const To = t.createElement("form"), oi = function(u) {
    return u instanceof RegExp || u instanceof Function;
  }, mn = function() {
    let u = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(_t && _t === u)) {
      if ((!u || typeof u != "object") && (u = {}), u = et(u), Et = // eslint-disable-next-line unicorn/prefer-includes
      ko.indexOf(u.PARSER_MEDIA_TYPE) === -1 ? Eo : u.PARSER_MEDIA_TYPE, Y = Et === "application/xhtml+xml" ? Dn : xt, F = Ae(u, "ALLOWED_TAGS") ? I({}, u.ALLOWED_TAGS, Y) : st, z = Ae(u, "ALLOWED_ATTR") ? I({}, u.ALLOWED_ATTR, Y) : me, dn = Ae(u, "ALLOWED_NAMESPACES") ? I({}, u.ALLOWED_NAMESPACES, Dn) : vo, un = Ae(u, "ADD_URI_SAFE_ATTR") ? I(
        et(li),
        // eslint-disable-line indent
        u.ADD_URI_SAFE_ATTR,
        // eslint-disable-line indent
        Y
        // eslint-disable-line indent
      ) : li, ni = Ae(u, "ADD_DATA_URI_TAGS") ? I(
        et(ii),
        // eslint-disable-line indent
        u.ADD_DATA_URI_TAGS,
        // eslint-disable-line indent
        Y
        // eslint-disable-line indent
      ) : ii, ct = Ae(u, "FORBID_CONTENTS") ? I({}, u.FORBID_CONTENTS, Y) : ti, Je = Ae(u, "FORBID_TAGS") ? I({}, u.FORBID_TAGS, Y) : {}, We = Ae(u, "FORBID_ATTR") ? I({}, u.FORBID_ATTR, Y) : {}, ft = Ae(u, "USE_PROFILES") ? u.USE_PROFILES : !1, Qe = u.ALLOW_ARIA_ATTR !== !1, wt = u.ALLOW_DATA_ATTR !== !1, Ve = u.ALLOW_UNKNOWN_PROTOCOLS || !1, xe = u.ALLOW_SELF_CLOSE_IN_ATTR !== !1, Ye = u.SAFE_FOR_TEMPLATES || !1, vt = u.SAFE_FOR_XML !== !1, we = u.WHOLE_DOCUMENT || !1, at = u.RETURN_DOM || !1, Mt = u.RETURN_DOM_FRAGMENT || !1, Pt = u.RETURN_TRUSTED_TYPE || !1, $e = u.FORCE_BODY || !1, $n = u.SANITIZE_DOM !== !1, ei = u.SANITIZE_NAMED_PROPS || !1, cn = u.KEEP_CONTENT !== !1, kt = u.IN_PLACE || !1, Oe = u.ALLOWED_URI_REGEXP || fo, ut = u.NAMESPACE || qe, v = u.CUSTOM_ELEMENT_HANDLING || {}, u.CUSTOM_ELEMENT_HANDLING && oi(u.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (v.tagNameCheck = u.CUSTOM_ELEMENT_HANDLING.tagNameCheck), u.CUSTOM_ELEMENT_HANDLING && oi(u.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (v.attributeNameCheck = u.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), u.CUSTOM_ELEMENT_HANDLING && typeof u.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (v.allowCustomizedBuiltInElements = u.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), Ye && (wt = !1), Mt && (at = !0), ft && (F = I({}, ml), z = [], ft.html === !0 && (I(F, dl), I(z, hl)), ft.svg === !0 && (I(F, In), I(z, Mn), I(z, Xt)), ft.svgFilters === !0 && (I(F, On), I(z, Mn), I(z, Xt)), ft.mathMl === !0 && (I(F, Nn), I(z, gl), I(z, Xt))), u.ADD_TAGS && (F === st && (F = et(F)), I(F, u.ADD_TAGS, Y)), u.ADD_ATTR && (z === me && (z = et(z)), I(z, u.ADD_ATTR, Y)), u.ADD_URI_SAFE_ATTR && I(un, u.ADD_URI_SAFE_ATTR, Y), u.FORBID_CONTENTS && (ct === ti && (ct = et(ct)), I(ct, u.FORBID_CONTENTS, Y)), cn && (F["#text"] = !0), we && I(F, ["html", "head", "body"]), F.table && (I(F, ["tbody"]), delete Je.tbody), u.TRUSTED_TYPES_POLICY) {
        if (typeof u.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw St('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof u.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw St('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        h = u.TRUSTED_TYPES_POLICY, N = h.createHTML("");
      } else
        h === void 0 && (h = Ka(m, l)), h !== null && typeof N == "string" && (N = h.createHTML(""));
      oe && oe(u), _t = u;
    }
  }, ri = I({}, ["mi", "mo", "mn", "ms", "mtext"]), si = I({}, ["foreignobject", "annotation-xml"]), yo = I({}, ["title", "style", "font", "a", "script"]), ai = I({}, [...In, ...On, ...za]), fi = I({}, [...Nn, ...qa]), Ao = function(u) {
    let g = b(u);
    (!g || !g.tagName) && (g = {
      namespaceURI: ut,
      tagName: "template"
    });
    const T = xt(u.tagName), U = xt(g.tagName);
    return dn[u.namespaceURI] ? u.namespaceURI === Ft ? g.namespaceURI === qe ? T === "svg" : g.namespaceURI === Ut ? T === "svg" && (U === "annotation-xml" || ri[U]) : !!ai[T] : u.namespaceURI === Ut ? g.namespaceURI === qe ? T === "math" : g.namespaceURI === Ft ? T === "math" && si[U] : !!fi[T] : u.namespaceURI === qe ? g.namespaceURI === Ft && !si[U] || g.namespaceURI === Ut && !ri[U] ? !1 : !fi[T] && (yo[T] || !ai[T]) : !!(Et === "application/xhtml+xml" && dn[u.namespaceURI]) : !1;
  }, Ne = function(u) {
    yt(e.removed, {
      element: u
    });
    try {
      b(u).removeChild(u);
    } catch {
      k(u);
    }
  }, zt = function(u, g) {
    try {
      yt(e.removed, {
        attribute: g.getAttributeNode(u),
        from: g
      });
    } catch {
      yt(e.removed, {
        attribute: null,
        from: g
      });
    }
    if (g.removeAttribute(u), u === "is" && !z[u])
      if (at || Mt)
        try {
          Ne(g);
        } catch {
        }
      else
        try {
          g.setAttribute(u, "");
        } catch {
        }
  }, ci = function(u) {
    let g = null, T = null;
    if ($e)
      u = "<remove></remove>" + u;
    else {
      const K = _l(u, /^[\r\n\t ]+/);
      T = K && K[0];
    }
    Et === "application/xhtml+xml" && ut === qe && (u = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + u + "</body></html>");
    const U = h ? h.createHTML(u) : u;
    if (ut === qe)
      try {
        g = new d().parseFromString(U, Et);
      } catch {
      }
    if (!g || !g.documentElement) {
      g = M.createDocument(ut, "template", null);
      try {
        g.documentElement.innerHTML = _n ? N : U;
      } catch {
      }
    }
    const $ = g.body || g.documentElement;
    return u && T && $.insertBefore(t.createTextNode(T), $.childNodes[0] || null), ut === qe ? S.call(g, we ? "html" : "body")[0] : we ? g.documentElement : $;
  }, ui = function(u) {
    return H.call(
      u.ownerDocument || u,
      u,
      // eslint-disable-next-line no-bitwise
      f.SHOW_ELEMENT | f.SHOW_COMMENT | f.SHOW_TEXT | f.SHOW_PROCESSING_INSTRUCTION | f.SHOW_CDATA_SECTION,
      null
    );
  }, _i = function(u) {
    return u instanceof _ && (typeof u.nodeName != "string" || typeof u.textContent != "string" || typeof u.removeChild != "function" || !(u.attributes instanceof c) || typeof u.removeAttribute != "function" || typeof u.setAttribute != "function" || typeof u.namespaceURI != "string" || typeof u.insertBefore != "function" || typeof u.hasChildNodes != "function");
  }, di = function(u) {
    return typeof a == "function" && u instanceof a;
  }, Be = function(u, g, T) {
    G[u] && Yt(G[u], (U) => {
      U.call(e, g, T, _t);
    });
  }, mi = function(u) {
    let g = null;
    if (Be("beforeSanitizeElements", u, null), _i(u))
      return Ne(u), !0;
    const T = Y(u.nodeName);
    if (Be("uponSanitizeElement", u, {
      tagName: T,
      allowedTags: F
    }), u.hasChildNodes() && !di(u.firstElementChild) && ie(/<[/\w]/g, u.innerHTML) && ie(/<[/\w]/g, u.textContent) || u.nodeType === Lt.progressingInstruction || vt && u.nodeType === Lt.comment && ie(/<[/\w]/g, u.data))
      return Ne(u), !0;
    if (!F[T] || Je[T]) {
      if (!Je[T] && gi(T) && (v.tagNameCheck instanceof RegExp && ie(v.tagNameCheck, T) || v.tagNameCheck instanceof Function && v.tagNameCheck(T)))
        return !1;
      if (cn && !ct[T]) {
        const U = b(u) || u.parentNode, $ = L(u) || u.childNodes;
        if ($ && U) {
          const K = $.length;
          for (let se = K - 1; se >= 0; --se) {
            const Me = E($[se], !0);
            Me.__removalCount = (u.__removalCount || 0) + 1, U.insertBefore(Me, p(u));
          }
        }
      }
      return Ne(u), !0;
    }
    return u instanceof s && !Ao(u) || (T === "noscript" || T === "noembed" || T === "noframes") && ie(/<\/no(script|embed|frames)/i, u.innerHTML) ? (Ne(u), !0) : (Ye && u.nodeType === Lt.text && (g = u.textContent, Yt([re, De, C], (U) => {
      g = At(g, U, " ");
    }), u.textContent !== g && (yt(e.removed, {
      element: u.cloneNode()
    }), u.textContent = g)), Be("afterSanitizeElements", u, null), !1);
  }, hi = function(u, g, T) {
    if ($n && (g === "id" || g === "name") && (T in t || T in To))
      return !1;
    if (!(wt && !We[g] && ie(V, g))) {
      if (!(Qe && ie(P, g))) {
        if (!z[g] || We[g]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(gi(u) && (v.tagNameCheck instanceof RegExp && ie(v.tagNameCheck, u) || v.tagNameCheck instanceof Function && v.tagNameCheck(u)) && (v.attributeNameCheck instanceof RegExp && ie(v.attributeNameCheck, g) || v.attributeNameCheck instanceof Function && v.attributeNameCheck(g)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            g === "is" && v.allowCustomizedBuiltInElements && (v.tagNameCheck instanceof RegExp && ie(v.tagNameCheck, T) || v.tagNameCheck instanceof Function && v.tagNameCheck(T)))
          ) return !1;
        } else if (!un[g]) {
          if (!ie(Oe, At(T, Ge, ""))) {
            if (!((g === "src" || g === "xlink:href" || g === "href") && u !== "script" && Ma(T, "data:") === 0 && ni[u])) {
              if (!(Ve && !ie(y, At(T, Ge, "")))) {
                if (T)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, gi = function(u) {
    return u !== "annotation-xml" && _l(u, Ie);
  }, pi = function(u) {
    Be("beforeSanitizeAttributes", u, null);
    const {
      attributes: g
    } = u;
    if (!g)
      return;
    const T = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: z
    };
    let U = g.length;
    for (; U--; ) {
      const $ = g[U], {
        name: K,
        namespaceURI: se,
        value: Me
      } = $, Tt = Y(K);
      let ne = K === "value" ? Me : Pa(Me);
      if (T.attrName = Tt, T.attrValue = ne, T.keepAttr = !0, T.forceKeepAttr = void 0, Be("uponSanitizeAttribute", u, T), ne = T.attrValue, vt && ie(/((--!?|])>)|<\/(style|title)/i, ne)) {
        zt(K, u);
        continue;
      }
      if (T.forceKeepAttr || (zt(K, u), !T.keepAttr))
        continue;
      if (!xe && ie(/\/>/i, ne)) {
        zt(K, u);
        continue;
      }
      Ye && Yt([re, De, C], (wi) => {
        ne = At(ne, wi, " ");
      });
      const bi = Y(u.nodeName);
      if (hi(bi, Tt, ne)) {
        if (ei && (Tt === "id" || Tt === "name") && (zt(K, u), ne = wo + ne), h && typeof m == "object" && typeof m.getAttributeType == "function" && !se)
          switch (m.getAttributeType(bi, Tt)) {
            case "TrustedHTML": {
              ne = h.createHTML(ne);
              break;
            }
            case "TrustedScriptURL": {
              ne = h.createScriptURL(ne);
              break;
            }
          }
        try {
          se ? u.setAttributeNS(se, K, ne) : u.setAttribute(K, ne), _i(u) ? Ne(u) : ul(e.removed);
        } catch {
        }
      }
    }
    Be("afterSanitizeAttributes", u, null);
  }, So = function A(u) {
    let g = null;
    const T = ui(u);
    for (Be("beforeSanitizeShadowDOM", u, null); g = T.nextNode(); )
      Be("uponSanitizeShadowNode", g, null), !mi(g) && (g.content instanceof o && A(g.content), pi(g));
    Be("afterSanitizeShadowDOM", u, null);
  };
  return e.sanitize = function(A) {
    let u = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, g = null, T = null, U = null, $ = null;
    if (_n = !A, _n && (A = "<!-->"), typeof A != "string" && !di(A))
      if (typeof A.toString == "function") {
        if (A = A.toString(), typeof A != "string")
          throw St("dirty is not a string, aborting");
      } else
        throw St("toString is not a function");
    if (!e.isSupported)
      return A;
    if (ve || mn(u), e.removed = [], typeof A == "string" && (kt = !1), kt) {
      if (A.nodeName) {
        const Me = Y(A.nodeName);
        if (!F[Me] || Je[Me])
          throw St("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (A instanceof a)
      g = ci("<!---->"), T = g.ownerDocument.importNode(A, !0), T.nodeType === Lt.element && T.nodeName === "BODY" || T.nodeName === "HTML" ? g = T : g.appendChild(T);
    else {
      if (!at && !Ye && !we && // eslint-disable-next-line unicorn/prefer-includes
      A.indexOf("<") === -1)
        return h && Pt ? h.createHTML(A) : A;
      if (g = ci(A), !g)
        return at ? null : Pt ? N : "";
    }
    g && $e && Ne(g.firstChild);
    const K = ui(kt ? A : g);
    for (; U = K.nextNode(); )
      mi(U) || (U.content instanceof o && So(U.content), pi(U));
    if (kt)
      return A;
    if (at) {
      if (Mt)
        for ($ = j.call(g.ownerDocument); g.firstChild; )
          $.appendChild(g.firstChild);
      else
        $ = g;
      return (z.shadowroot || z.shadowrootmode) && ($ = ce.call(n, $, !0)), $;
    }
    let se = we ? g.outerHTML : g.innerHTML;
    return we && F["!doctype"] && g.ownerDocument && g.ownerDocument.doctype && g.ownerDocument.doctype.name && ie(co, g.ownerDocument.doctype.name) && (se = "<!DOCTYPE " + g.ownerDocument.doctype.name + `>
` + se), Ye && Yt([re, De, C], (Me) => {
      se = At(se, Me, " ");
    }), h && Pt ? h.createHTML(se) : se;
  }, e.setConfig = function() {
    let A = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    mn(A), ve = !0;
  }, e.clearConfig = function() {
    _t = null, ve = !1;
  }, e.isValidAttribute = function(A, u, g) {
    _t || mn({});
    const T = Y(A), U = Y(u);
    return hi(T, U, g);
  }, e.addHook = function(A, u) {
    typeof u == "function" && (G[A] = G[A] || [], yt(G[A], u));
  }, e.removeHook = function(A) {
    if (G[A])
      return ul(G[A]);
  }, e.removeHooks = function(A) {
    G[A] && (G[A] = []);
  }, e.removeAllHooks = function() {
    G = {};
  }, e;
}
uo();
const {
  SvelteComponent: Ja,
  attr: Qa,
  detach: _o,
  element: xa,
  empty: $a,
  init: ef,
  insert: mo,
  noop: bl,
  safe_not_equal: tf,
  set_style: wl
} = window.__gradio__svelte__internal;
function vl(i) {
  let e, t = `${/*time_limit*/
  i[0]}s`;
  return {
    c() {
      e = xa("div"), Qa(e, "class", "streaming-bar svelte-ga0jj6"), wl(e, "animation-duration", t);
    },
    m(n, l) {
      mo(n, e, l);
    },
    p(n, l) {
      l & /*time_limit*/
      1 && t !== (t = `${/*time_limit*/
      n[0]}s`) && wl(e, "animation-duration", t);
    },
    d(n) {
      n && _o(e);
    }
  };
}
function nf(i) {
  let e, t = (
    /*time_limit*/
    i[0] && vl(i)
  );
  return {
    c() {
      t && t.c(), e = $a();
    },
    m(n, l) {
      t && t.m(n, l), mo(n, e, l);
    },
    p(n, [l]) {
      /*time_limit*/
      n[0] ? t ? t.p(n, l) : (t = vl(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    i: bl,
    o: bl,
    d(n) {
      n && _o(e), t && t.d(n);
    }
  };
}
function lf(i, e, t) {
  let { time_limit: n } = e;
  return i.$$set = (l) => {
    "time_limit" in l && t(0, n = l.time_limit);
  }, [n];
}
class of extends Ja {
  constructor(e) {
    super(), ef(this, e, lf, nf, tf, { time_limit: 0 });
  }
}
const {
  SvelteComponent: rf,
  append: Zt,
  attr: Pn,
  create_component: sf,
  destroy_component: af,
  detach: ff,
  element: Un,
  init: cf,
  insert: uf,
  listen: _f,
  mount_component: df,
  noop: mf,
  safe_not_equal: hf,
  set_style: gf,
  space: pf,
  text: bf,
  transition_in: wf,
  transition_out: vf
} = window.__gradio__svelte__internal, { createEventDispatcher: kf } = window.__gradio__svelte__internal;
function Ef(i) {
  let e, t, n, l, o, r = "Click to Access Webcam", a, s, f, c;
  return l = new Ts({}), {
    c() {
      e = Un("button"), t = Un("div"), n = Un("span"), sf(l.$$.fragment), o = pf(), a = bf(r), Pn(n, "class", "icon-wrap svelte-fjcd9c"), Pn(t, "class", "wrap svelte-fjcd9c"), Pn(e, "class", "svelte-fjcd9c"), gf(e, "height", "100%");
    },
    m(_, d) {
      uf(_, e, d), Zt(e, t), Zt(t, n), df(l, n, null), Zt(t, o), Zt(t, a), s = !0, f || (c = _f(
        e,
        "click",
        /*click_handler*/
        i[1]
      ), f = !0);
    },
    p: mf,
    i(_) {
      s || (wf(l.$$.fragment, _), s = !0);
    },
    o(_) {
      vf(l.$$.fragment, _), s = !1;
    },
    d(_) {
      _ && ff(e), af(l), f = !1, c();
    }
  };
}
function Tf(i) {
  const e = kf();
  return [e, () => e("click")];
}
class yf extends rf {
  constructor(e) {
    super(), cf(this, e, Tf, Ef, hf, {});
  }
}
function Af() {
  return navigator.mediaDevices.enumerateDevices();
}
function Sf(i, e) {
  e.srcObject = i, e.muted = !0, e.play();
}
async function kl(i, e, t) {
  const n = {
    width: { ideal: 1920 },
    height: { ideal: 1440 }
  }, l = {
    video: t ? { deviceId: { exact: t }, ...n } : n,
    audio: i
  };
  return navigator.mediaDevices.getUserMedia(l).then((o) => (Sf(o, e), o));
}
function Cf(i) {
  return i.filter(
    (t) => t.kind === "videoinput"
  );
}
function Lf(i, e) {
  return i.addEventListener(
    "icegatheringstatechange",
    () => {
      console.log(i.iceGatheringState);
    },
    !1
  ), i.addEventListener(
    "iceconnectionstatechange",
    () => {
      console.log(i.iceConnectionState);
    },
    !1
  ), i.addEventListener(
    "signalingstatechange",
    () => {
      console.log(i.signalingState);
    },
    !1
  ), i.addEventListener("track", (t) => {
    console.log("track event listener"), t.track.kind == "video" && (console.log("streams", t.streams), e.srcObject = t.streams[0], console.log("node.srcOject", e.srcObject));
  }), i;
}
async function Rf(i, e, t, n, l) {
  return e = Lf(e, t), i ? i.getTracks().forEach((o) => {
    o.applyConstraints({ frameRate: { max: 30 } }), console.log("Track stream callback", o), e.addTrack(o, i);
  }) : (console.log("Creating transceiver!"), e.addTransceiver("video", { direction: "recvonly" })), await If(e, n, l), e;
}
function Df(i, e) {
  return new Promise((t, n) => {
    i(e).then((l) => {
      console.log("data", l), (l == null ? void 0 : l.status) === "failed" && (console.log("rejecting"), n("error")), t(l);
    });
  });
}
async function If(i, e, t) {
  return i.createOffer().then((n) => i.setLocalDescription(n)).then(() => new Promise((n) => {
    if (console.log("ice gathering state", i.iceGatheringState), i.iceGatheringState === "complete")
      n();
    else {
      const l = () => {
        i.iceGatheringState === "complete" && (console.log("ice complete"), i.removeEventListener("icegatheringstatechange", l), n());
      };
      i.addEventListener("icegatheringstatechange", l);
    }
  })).then(() => {
    var n = i.localDescription;
    return Df(
      e,
      {
        sdp: n.sdp,
        type: n.type,
        webrtc_id: t
      }
    );
  }).then((n) => n).then((n) => i.setRemoteDescription(n));
}
function Of(i) {
  console.log("pc", i), console.log("STOPPING"), i.getTransceivers && i.getTransceivers().forEach((e) => {
    e.stop && e.stop();
  }), i.getSenders() && i.getSenders().forEach((e) => {
    e.track && e.track.stop && e.track.stop();
  }), setTimeout(() => {
    i.close();
  }, 500);
}
const {
  SvelteComponent: Nf,
  action_destroyer: Mf,
  add_render_callback: Pf,
  append: W,
  attr: B,
  binding_callbacks: Uf,
  check_outros: Xn,
  create_component: lt,
  create_in_transition: Ff,
  destroy_component: ot,
  destroy_each: zf,
  detach: ue,
  element: te,
  empty: ho,
  ensure_array_like: El,
  group_outros: Zn,
  init: qf,
  insert: _e,
  listen: nn,
  mount_component: rt,
  noop: go,
  run_all: Bf,
  safe_not_equal: Hf,
  set_data: Ot,
  set_input_value: Kn,
  set_style: po,
  space: je,
  stop_propagation: jf,
  text: Nt,
  toggle_class: Kt,
  transition_in: le,
  transition_out: fe
} = window.__gradio__svelte__internal, { createEventDispatcher: Gf, onMount: Wf } = window.__gradio__svelte__internal;
function Tl(i, e, t) {
  const n = i.slice();
  return n[29] = e[t], n;
}
function Vf(i) {
  let e, t, n, l, o, r, a, s, f, c;
  const _ = [Kf, Zf, Xf], d = [];
  function m(k, p) {
    return (
      /*stream_state*/
      k[6] === "waiting" ? 0 : (
        /*stream_state*/
        k[6] === "open" ? 1 : 2
      )
    );
  }
  n = m(i), l = d[n] = _[n](i);
  let w = Jf(i), E = (
    /*options_open*/
    i[8] && /*selected_device*/
    i[4] && yl(i)
  );
  return {
    c() {
      e = te("div"), t = te("button"), l.c(), o = je(), w && w.c(), r = je(), E && E.c(), a = ho(), B(t, "aria-label", "start stream"), B(t, "class", "svelte-1ljlr19"), B(e, "class", "button-wrap svelte-1ljlr19");
    },
    m(k, p) {
      _e(k, e, p), W(e, t), d[n].m(t, null), W(e, o), w && w.m(e, null), _e(k, r, p), E && E.m(k, p), _e(k, a, p), s = !0, f || (c = nn(
        t,
        "click",
        /*start_webrtc*/
        i[11]
      ), f = !0);
    },
    p(k, p) {
      let L = n;
      n = m(k), n === L ? d[n].p(k, p) : (Zn(), fe(d[L], 1, 1, () => {
        d[L] = null;
      }), Xn(), l = d[n], l ? l.p(k, p) : (l = d[n] = _[n](k), l.c()), le(l, 1), l.m(t, null)), w.p(k, p), /*options_open*/
      k[8] && /*selected_device*/
      k[4] ? E ? (E.p(k, p), p[0] & /*options_open, selected_device*/
      272 && le(E, 1)) : (E = yl(k), E.c(), le(E, 1), E.m(a.parentNode, a)) : E && (Zn(), fe(E, 1, 1, () => {
        E = null;
      }), Xn());
    },
    i(k) {
      s || (le(l), le(w), le(E), s = !0);
    },
    o(k) {
      fe(l), fe(w), fe(E), s = !1;
    },
    d(k) {
      k && (ue(e), ue(r), ue(a)), d[n].d(), w && w.d(), E && E.d(k), f = !1, c();
    }
  };
}
function Yf(i) {
  let e, t, n, l;
  return t = new yf({}), t.$on(
    "click",
    /*click_handler*/
    i[21]
  ), {
    c() {
      e = te("div"), lt(t.$$.fragment), B(e, "title", "grant webcam access"), po(e, "height", "100%");
    },
    m(o, r) {
      _e(o, e, r), rt(t, e, null), l = !0;
    },
    p: go,
    i(o) {
      l || (le(t.$$.fragment, o), o && (n || Pf(() => {
        n = Ff(e, Ks, { delay: 100, duration: 200 }), n.start();
      })), l = !0);
    },
    o(o) {
      fe(t.$$.fragment, o), l = !1;
    },
    d(o) {
      o && ue(e), ot(t);
    }
  };
}
function Xf(i) {
  let e, t, n, l, o = (
    /*i18n*/
    i[0]("audio.record") + ""
  ), r, a;
  return n = new Ar({}), {
    c() {
      e = te("div"), t = te("div"), lt(n.$$.fragment), l = je(), r = Nt(o), B(t, "class", "icon color-primary svelte-1ljlr19"), B(t, "title", "start recording"), B(e, "class", "icon-with-text svelte-1ljlr19");
    },
    m(s, f) {
      _e(s, e, f), W(e, t), rt(n, t, null), W(e, l), W(e, r), a = !0;
    },
    p(s, f) {
      (!a || f[0] & /*i18n*/
      1) && o !== (o = /*i18n*/
      s[0]("audio.record") + "") && Ot(r, o);
    },
    i(s) {
      a || (le(n.$$.fragment, s), a = !0);
    },
    o(s) {
      fe(n.$$.fragment, s), a = !1;
    },
    d(s) {
      s && ue(e), ot(n);
    }
  };
}
function Zf(i) {
  let e, t, n, l, o = (
    /*i18n*/
    i[0]("audio.stop") + ""
  ), r, a;
  return n = new ns({}), {
    c() {
      e = te("div"), t = te("div"), lt(n.$$.fragment), l = je(), r = Nt(o), B(t, "class", "icon color-primary svelte-1ljlr19"), B(t, "title", "stop recording"), B(e, "class", "icon-with-text svelte-1ljlr19");
    },
    m(s, f) {
      _e(s, e, f), W(e, t), rt(n, t, null), W(e, l), W(e, r), a = !0;
    },
    p(s, f) {
      (!a || f[0] & /*i18n*/
      1) && o !== (o = /*i18n*/
      s[0]("audio.stop") + "") && Ot(r, o);
    },
    i(s) {
      a || (le(n.$$.fragment, s), a = !0);
    },
    o(s) {
      fe(n.$$.fragment, s), a = !1;
    },
    d(s) {
      s && ue(e), ot(n);
    }
  };
}
function Kf(i) {
  let e, t, n, l, o = (
    /*i18n*/
    i[0]("audio.waiting") + ""
  ), r, a;
  return n = new Ds({}), {
    c() {
      e = te("div"), t = te("div"), lt(n.$$.fragment), l = je(), r = Nt(o), B(t, "class", "icon color-primary svelte-1ljlr19"), B(t, "title", "spinner"), B(e, "class", "icon-with-text svelte-1ljlr19"), po(e, "width", "var(--size-24)");
    },
    m(s, f) {
      _e(s, e, f), W(e, t), rt(n, t, null), W(e, l), W(e, r), a = !0;
    },
    p(s, f) {
      (!a || f[0] & /*i18n*/
      1) && o !== (o = /*i18n*/
      s[0]("audio.waiting") + "") && Ot(r, o);
    },
    i(s) {
      a || (le(n.$$.fragment, s), a = !0);
    },
    o(s) {
      fe(n.$$.fragment, s), a = !1;
    },
    d(s) {
      s && ue(e), ot(n);
    }
  };
}
function Jf(i) {
  let e, t, n, l, o;
  return t = new Wl({}), {
    c() {
      e = te("button"), lt(t.$$.fragment), B(e, "class", "icon svelte-1ljlr19"), B(e, "aria-label", "select input source");
    },
    m(r, a) {
      _e(r, e, a), rt(t, e, null), n = !0, l || (o = nn(
        e,
        "click",
        /*click_handler_1*/
        i[22]
      ), l = !0);
    },
    p: go,
    i(r) {
      n || (le(t.$$.fragment, r), n = !0);
    },
    o(r) {
      fe(t.$$.fragment, r), n = !1;
    },
    d(r) {
      r && ue(e), ot(t), l = !1, o();
    }
  };
}
function yl(i) {
  let e, t, n, l, o, r, a;
  n = new Wl({});
  function s(_, d) {
    return (
      /*available_video_devices*/
      _[3].length === 0 ? xf : Qf
    );
  }
  let f = s(i), c = f(i);
  return {
    c() {
      e = te("select"), t = te("button"), lt(n.$$.fragment), l = je(), c.c(), B(t, "class", "inset-icon svelte-1ljlr19"), B(e, "class", "select-wrap svelte-1ljlr19"), B(e, "aria-label", "select source");
    },
    m(_, d) {
      _e(_, e, d), W(e, t), rt(n, t, null), W(t, l), c.m(e, null), o = !0, r || (a = [
        nn(t, "click", jf(
          /*click_handler_2*/
          i[23]
        )),
        Mf(Jn.call(
          null,
          e,
          /*handle_click_outside*/
          i[12]
        )),
        nn(
          e,
          "change",
          /*handle_device_change*/
          i[9]
        )
      ], r = !0);
    },
    p(_, d) {
      f === (f = s(_)) && c ? c.p(_, d) : (c.d(1), c = f(_), c && (c.c(), c.m(e, null)));
    },
    i(_) {
      o || (le(n.$$.fragment, _), o = !0);
    },
    o(_) {
      fe(n.$$.fragment, _), o = !1;
    },
    d(_) {
      _ && ue(e), ot(n), c.d(), r = !1, Bf(a);
    }
  };
}
function Qf(i) {
  let e, t = El(
    /*available_video_devices*/
    i[3]
  ), n = [];
  for (let l = 0; l < t.length; l += 1)
    n[l] = Al(Tl(i, t, l));
  return {
    c() {
      for (let l = 0; l < n.length; l += 1)
        n[l].c();
      e = ho();
    },
    m(l, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(l, o);
      _e(l, e, o);
    },
    p(l, o) {
      if (o[0] & /*available_video_devices, selected_device*/
      24) {
        t = El(
          /*available_video_devices*/
          l[3]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const a = Tl(l, t, r);
          n[r] ? n[r].p(a, o) : (n[r] = Al(a), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(l) {
      l && ue(e), zf(n, l);
    }
  };
}
function xf(i) {
  let e, t = (
    /*i18n*/
    i[0]("common.no_devices") + ""
  ), n;
  return {
    c() {
      e = te("option"), n = Nt(t), e.__value = "", Kn(e, e.__value), B(e, "class", "svelte-1ljlr19");
    },
    m(l, o) {
      _e(l, e, o), W(e, n);
    },
    p(l, o) {
      o[0] & /*i18n*/
      1 && t !== (t = /*i18n*/
      l[0]("common.no_devices") + "") && Ot(n, t);
    },
    d(l) {
      l && ue(e);
    }
  };
}
function Al(i) {
  let e, t = (
    /*device*/
    i[29].label + ""
  ), n, l, o, r;
  return {
    c() {
      e = te("option"), n = Nt(t), l = je(), e.__value = o = /*device*/
      i[29].deviceId, Kn(e, e.__value), e.selected = r = /*selected_device*/
      i[4].deviceId === /*device*/
      i[29].deviceId, B(e, "class", "svelte-1ljlr19");
    },
    m(a, s) {
      _e(a, e, s), W(e, n), W(e, l);
    },
    p(a, s) {
      s[0] & /*available_video_devices*/
      8 && t !== (t = /*device*/
      a[29].label + "") && Ot(n, t), s[0] & /*available_video_devices*/
      8 && o !== (o = /*device*/
      a[29].deviceId) && (e.__value = o, Kn(e, e.__value)), s[0] & /*selected_device, available_video_devices*/
      24 && r !== (r = /*selected_device*/
      a[4].deviceId === /*device*/
      a[29].deviceId) && (e.selected = r);
    },
    d(a) {
      a && ue(e);
    }
  };
}
function $f(i) {
  let e, t, n, l, o, r, a, s;
  t = new of({
    props: { time_limit: (
      /*_time_limit*/
      i[5]
    ) }
  });
  const f = [Yf, Vf], c = [];
  function _(d, m) {
    return (
      /*webcam_accessed*/
      d[7] ? 1 : 0
    );
  }
  return r = _(i), a = c[r] = f[r](i), {
    c() {
      e = te("div"), lt(t.$$.fragment), n = je(), l = te("video"), o = je(), a.c(), l.autoplay = !0, l.playsInline = !0, B(l, "class", "svelte-1ljlr19"), Kt(l, "hide", !/*webcam_accessed*/
      i[7]), Kt(
        l,
        "flip",
        /*stream_state*/
        i[6] != "open"
      ), B(e, "class", "wrap svelte-1ljlr19");
    },
    m(d, m) {
      _e(d, e, m), rt(t, e, null), W(e, n), W(e, l), i[20](l), W(e, o), c[r].m(e, null), s = !0;
    },
    p(d, m) {
      const w = {};
      m[0] & /*_time_limit*/
      32 && (w.time_limit = /*_time_limit*/
      d[5]), t.$set(w), (!s || m[0] & /*webcam_accessed*/
      128) && Kt(l, "hide", !/*webcam_accessed*/
      d[7]), (!s || m[0] & /*stream_state*/
      64) && Kt(
        l,
        "flip",
        /*stream_state*/
        d[6] != "open"
      );
      let E = r;
      r = _(d), r === E ? c[r].p(d, m) : (Zn(), fe(c[E], 1, 1, () => {
        c[E] = null;
      }), Xn(), a = c[r], a ? a.p(d, m) : (a = c[r] = f[r](d), a.c()), le(a, 1), a.m(e, null));
    },
    i(d) {
      s || (le(t.$$.fragment, d), le(a), s = !0);
    },
    o(d) {
      fe(t.$$.fragment, d), fe(a), s = !1;
    },
    d(d) {
      d && ue(e), ot(t), i[20](null), c[r].d();
    }
  };
}
function Jn(i, e) {
  const t = (n) => {
    i && !i.contains(n.target) && !n.defaultPrevented && e(n);
  };
  return document.addEventListener("click", t, !0), {
    destroy() {
      document.removeEventListener("click", t, !0);
    }
  };
}
function ec(i, e, t) {
  var n = this && this.__awaiter || function(C, V, P, y) {
    function Ge(Ie) {
      return Ie instanceof P ? Ie : new P(function(Oe) {
        Oe(Ie);
      });
    }
    return new (P || (P = Promise))(function(Ie, Oe) {
      function F(me) {
        try {
          z(y.next(me));
        } catch (v) {
          Oe(v);
        }
      }
      function st(me) {
        try {
          z(y.throw(me));
        } catch (v) {
          Oe(v);
        }
      }
      function z(me) {
        me.done ? Ie(me.value) : Ge(me.value).then(F, st);
      }
      z((y = y.apply(C, V || [])).next());
    });
  };
  let l, o = [], r = null, a = null, { time_limit: s = null } = e, f = "closed";
  const c = Math.random().toString(36).substring(2), _ = (C) => {
    C === "closed" ? (t(5, a = null), t(6, f = "closed")) : C === "waiting" ? t(6, f = "waiting") : t(6, f = "open");
  };
  let { rtc_configuration: d } = e, { stream_every: m = 1 } = e, { server: w } = e, { include_audio: E } = e, { i18n: k } = e;
  const p = Gf();
  Wf(() => document.createElement("canvas"));
  const L = (C) => n(void 0, void 0, void 0, function* () {
    const P = C.target.value;
    yield kl(E, l, P).then((y) => n(void 0, void 0, void 0, function* () {
      h = y, t(4, r = o.find((Ge) => Ge.deviceId === P) || null), t(8, j = !1);
    }));
  });
  function b() {
    return n(this, void 0, void 0, function* () {
      try {
        kl(E, l).then((C) => n(this, void 0, void 0, function* () {
          t(7, N = !0), t(3, o = yield Af()), h = C;
        })).then(() => Cf(o)).then((C) => {
          t(3, o = C);
          const V = h.getTracks().map((P) => {
            var y;
            return (y = P.getSettings()) === null || y === void 0 ? void 0 : y.deviceId;
          })[0];
          t(4, r = V && C.find((P) => P.deviceId === V) || o[0]);
        }), (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) && p("error", k("image.no_webcam_support"));
      } catch (C) {
        if (C instanceof DOMException && C.name == "NotAllowedError")
          p("error", k("image.allow_webcam_access"));
        else
          throw C;
      }
    });
  }
  let h, N = !1, M;
  function H() {
    return n(this, void 0, void 0, function* () {
      if (f === "closed") {
        const V = d || {
          iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
        };
        console.log("config", V), M = new RTCPeerConnection(V), M.addEventListener("connectionstatechange", (P) => n(this, void 0, void 0, function* () {
          switch (M.connectionState) {
            case "connected":
              t(6, f = "open"), t(5, a = s);
              break;
            case "disconnected":
              t(6, f = "closed"), yield b();
              break;
          }
        })), t(6, f = "waiting"), Rf(h, M, l, w.offer, c).then((P) => {
          M = P;
        }).catch(() => {
          console.log("catching"), t(6, f = "closed"), p("error", "Too many concurrent users. Come back later!");
        });
      } else
        Of(M), t(6, f = "closed"), yield b();
    });
  }
  window.setInterval(
    () => {
      f == "open" && (console.log("dispatching tick"), p("tick"));
    },
    m * 1e3
  );
  let j = !1;
  function S(C) {
    C.preventDefault(), C.stopPropagation(), t(8, j = !1);
  }
  function ce(C) {
    Uf[C ? "unshift" : "push"](() => {
      l = C, t(2, l);
    });
  }
  const G = async () => b(), re = () => t(8, j = !0), De = () => t(8, j = !1);
  return i.$$set = (C) => {
    "time_limit" in C && t(13, s = C.time_limit), "rtc_configuration" in C && t(16, d = C.rtc_configuration), "stream_every" in C && t(17, m = C.stream_every), "server" in C && t(18, w = C.server), "include_audio" in C && t(19, E = C.include_audio), "i18n" in C && t(0, k = C.i18n);
  }, [
    k,
    Jn,
    l,
    o,
    r,
    a,
    f,
    N,
    j,
    L,
    b,
    H,
    S,
    s,
    c,
    _,
    d,
    m,
    w,
    E,
    ce,
    G,
    re,
    De
  ];
}
class tc extends Nf {
  constructor(e) {
    super(), qf(
      this,
      e,
      ec,
      $f,
      Hf,
      {
        time_limit: 13,
        webrtc_id: 14,
        modify_stream: 15,
        rtc_configuration: 16,
        stream_every: 17,
        server: 18,
        include_audio: 19,
        i18n: 0,
        click_outside: 1
      },
      null,
      [-1, -1]
    );
  }
  get webrtc_id() {
    return this.$$.ctx[14];
  }
  get modify_stream() {
    return this.$$.ctx[15];
  }
  get click_outside() {
    return Jn;
  }
}
const {
  SvelteComponent: nc,
  add_flush_callback: ic,
  attr: Sl,
  bind: lc,
  binding_callbacks: oc,
  bubble: Jt,
  create_component: Cl,
  destroy_component: Ll,
  detach: Rl,
  element: rc,
  init: sc,
  insert: Dl,
  mount_component: Il,
  safe_not_equal: ac,
  space: fc,
  transition_in: Ol,
  transition_out: Nl
} = window.__gradio__svelte__internal, { createEventDispatcher: cc } = window.__gradio__svelte__internal;
function uc(i) {
  let e, t, n, l, o, r;
  e = new lr({
    props: {
      show_label: (
        /*show_label*/
        i[2]
      ),
      Icon: gs,
      label: (
        /*label*/
        i[1] || "Video"
      )
    }
  });
  function a(f) {
    i[11](f);
  }
  let s = {
    rtc_configuration: (
      /*rtc_configuration*/
      i[7]
    ),
    include_audio: (
      /*include_audio*/
      i[3]
    ),
    time_limit: (
      /*time_limit*/
      i[5]
    ),
    i18n: (
      /*i18n*/
      i[4]
    ),
    stream_every: 0.5,
    server: (
      /*server*/
      i[6]
    )
  };
  return (
    /*value*/
    i[0] !== void 0 && (s.webrtc_id = /*value*/
    i[0]), l = new tc({ props: s }), oc.push(() => lc(l, "webrtc_id", a)), l.$on(
      "error",
      /*error_handler*/
      i[12]
    ), l.$on(
      "start_recording",
      /*start_recording_handler*/
      i[13]
    ), l.$on(
      "stop_recording",
      /*stop_recording_handler*/
      i[14]
    ), l.$on(
      "tick",
      /*tick_handler*/
      i[15]
    ), {
      c() {
        Cl(e.$$.fragment), t = fc(), n = rc("div"), Cl(l.$$.fragment), Sl(n, "data-testid", "video"), Sl(n, "class", "video-container svelte-1kyjvp4");
      },
      m(f, c) {
        Il(e, f, c), Dl(f, t, c), Dl(f, n, c), Il(l, n, null), r = !0;
      },
      p(f, [c]) {
        const _ = {};
        c & /*show_label*/
        4 && (_.show_label = /*show_label*/
        f[2]), c & /*label*/
        2 && (_.label = /*label*/
        f[1] || "Video"), e.$set(_);
        const d = {};
        c & /*rtc_configuration*/
        128 && (d.rtc_configuration = /*rtc_configuration*/
        f[7]), c & /*include_audio*/
        8 && (d.include_audio = /*include_audio*/
        f[3]), c & /*time_limit*/
        32 && (d.time_limit = /*time_limit*/
        f[5]), c & /*i18n*/
        16 && (d.i18n = /*i18n*/
        f[4]), c & /*server*/
        64 && (d.server = /*server*/
        f[6]), !o && c & /*value*/
        1 && (o = !0, d.webrtc_id = /*value*/
        f[0], ic(() => o = !1)), l.$set(d);
      },
      i(f) {
        r || (Ol(e.$$.fragment, f), Ol(l.$$.fragment, f), r = !0);
      },
      o(f) {
        Nl(e.$$.fragment, f), Nl(l.$$.fragment, f), r = !1;
      },
      d(f) {
        f && (Rl(t), Rl(n)), Ll(e, f), Ll(l);
      }
    }
  );
}
let _c = !1;
function dc(i, e, t) {
  let { value: n = null } = e, { label: l = void 0 } = e, { show_label: o = !0 } = e, { include_audio: r } = e, { i18n: a } = e, { active_source: s = "webcam" } = e, { handle_reset_value: f = () => {
  } } = e, { stream_handler: c } = e, { time_limit: _ = null } = e, { server: d } = e, { rtc_configuration: m } = e;
  const w = cc();
  function E(h) {
    n = h, t(0, n);
  }
  function k(h) {
    Jt.call(this, i, h);
  }
  function p(h) {
    Jt.call(this, i, h);
  }
  function L(h) {
    Jt.call(this, i, h);
  }
  function b(h) {
    Jt.call(this, i, h);
  }
  return i.$$set = (h) => {
    "value" in h && t(0, n = h.value), "label" in h && t(1, l = h.label), "show_label" in h && t(2, o = h.show_label), "include_audio" in h && t(3, r = h.include_audio), "i18n" in h && t(4, a = h.i18n), "active_source" in h && t(8, s = h.active_source), "handle_reset_value" in h && t(9, f = h.handle_reset_value), "stream_handler" in h && t(10, c = h.stream_handler), "time_limit" in h && t(5, _ = h.time_limit), "server" in h && t(6, d = h.server), "rtc_configuration" in h && t(7, m = h.rtc_configuration);
  }, i.$$.update = () => {
    i.$$.dirty & /*value*/
    1 && console.log("interactive value", n);
  }, w("drag", _c), [
    n,
    l,
    o,
    r,
    a,
    _,
    d,
    m,
    s,
    f,
    c,
    E,
    k,
    p,
    L,
    b
  ];
}
class mc extends nc {
  constructor(e) {
    super(), sc(this, e, dc, uc, ac, {
      value: 0,
      label: 1,
      show_label: 2,
      include_audio: 3,
      i18n: 4,
      active_source: 8,
      handle_reset_value: 9,
      stream_handler: 10,
      time_limit: 5,
      server: 6,
      rtc_configuration: 7
    });
  }
}
var Ml;
(function(i) {
  i.LOAD = "LOAD", i.EXEC = "EXEC", i.WRITE_FILE = "WRITE_FILE", i.READ_FILE = "READ_FILE", i.DELETE_FILE = "DELETE_FILE", i.RENAME = "RENAME", i.CREATE_DIR = "CREATE_DIR", i.LIST_DIR = "LIST_DIR", i.DELETE_DIR = "DELETE_DIR", i.ERROR = "ERROR", i.DOWNLOAD = "DOWNLOAD", i.PROGRESS = "PROGRESS", i.LOG = "LOG", i.MOUNT = "MOUNT", i.UNMOUNT = "UNMOUNT";
})(Ml || (Ml = {}));
const Hc = (i) => {
  let e = ["B", "KB", "MB", "GB", "PB"], t = 0;
  for (; i > 1024; )
    i /= 1024, t++;
  let n = e[t];
  return i.toFixed(1) + " " + n;
}, jc = () => !0;
function Gc(i, { autoplay: e }) {
  async function t() {
    e && await i.play();
  }
  return i.addEventListener("loadeddata", t), {
    destroy() {
      i.removeEventListener("loadeddata", t);
    }
  };
}
const {
  SvelteComponent: hc,
  append: gc,
  attr: Fn,
  binding_callbacks: pc,
  detach: Qn,
  element: Pl,
  empty: bo,
  init: bc,
  insert: xn,
  is_function: Ul,
  listen: zn,
  noop: Fl,
  run_all: wc,
  safe_not_equal: vc,
  set_data: Wc,
  src_url_equal: zl,
  text: Vc,
  toggle_class: ht
} = window.__gradio__svelte__internal;
function ql(i) {
  let e;
  function t(o, r) {
    return kc;
  }
  let l = t()(i);
  return {
    c() {
      l.c(), e = bo();
    },
    m(o, r) {
      l.m(o, r), xn(o, e, r);
    },
    p(o, r) {
      l.p(o, r);
    },
    d(o) {
      o && Qn(e), l.d(o);
    }
  };
}
function kc(i) {
  let e, t, n, l, o;
  return {
    c() {
      var r;
      e = Pl("div"), t = Pl("video"), zl(t.src, n = /*value*/
      (r = i[2]) == null ? void 0 : r.video.url) || Fn(t, "src", n), Fn(e, "class", "container svelte-13u05e4"), ht(
        e,
        "table",
        /*type*/
        i[0] === "table"
      ), ht(
        e,
        "gallery",
        /*type*/
        i[0] === "gallery"
      ), ht(
        e,
        "selected",
        /*selected*/
        i[1]
      );
    },
    m(r, a) {
      xn(r, e, a), gc(e, t), i[6](t), l || (o = [
        zn(
          t,
          "loadeddata",
          /*init*/
          i[4]
        ),
        zn(t, "mouseover", function() {
          Ul(
            /*video*/
            i[3].play.bind(
              /*video*/
              i[3]
            )
          ) && i[3].play.bind(
            /*video*/
            i[3]
          ).apply(this, arguments);
        }),
        zn(t, "mouseout", function() {
          Ul(
            /*video*/
            i[3].pause.bind(
              /*video*/
              i[3]
            )
          ) && i[3].pause.bind(
            /*video*/
            i[3]
          ).apply(this, arguments);
        })
      ], l = !0);
    },
    p(r, a) {
      var s;
      i = r, a & /*value*/
      4 && !zl(t.src, n = /*value*/
      (s = i[2]) == null ? void 0 : s.video.url) && Fn(t, "src", n), a & /*type*/
      1 && ht(
        e,
        "table",
        /*type*/
        i[0] === "table"
      ), a & /*type*/
      1 && ht(
        e,
        "gallery",
        /*type*/
        i[0] === "gallery"
      ), a & /*selected*/
      2 && ht(
        e,
        "selected",
        /*selected*/
        i[1]
      );
    },
    d(r) {
      r && Qn(e), i[6](null), l = !1, wc(o);
    }
  };
}
function Ec(i) {
  let e, t = (
    /*value*/
    i[2] && ql(i)
  );
  return {
    c() {
      t && t.c(), e = bo();
    },
    m(n, l) {
      t && t.m(n, l), xn(n, e, l);
    },
    p(n, [l]) {
      /*value*/
      n[2] ? t ? t.p(n, l) : (t = ql(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    i: Fl,
    o: Fl,
    d(n) {
      n && Qn(e), t && t.d(n);
    }
  };
}
function Tc(i, e, t) {
  var n = this && this.__awaiter || function(_, d, m, w) {
    function E(k) {
      return k instanceof m ? k : new m(function(p) {
        p(k);
      });
    }
    return new (m || (m = Promise))(function(k, p) {
      function L(N) {
        try {
          h(w.next(N));
        } catch (M) {
          p(M);
        }
      }
      function b(N) {
        try {
          h(w.throw(N));
        } catch (M) {
          p(M);
        }
      }
      function h(N) {
        N.done ? k(N.value) : E(N.value).then(L, b);
      }
      h((w = w.apply(_, d || [])).next());
    });
  };
  let { type: l } = e, { selected: o = !1 } = e, { value: r } = e, { loop: a } = e, s;
  function f() {
    return n(this, void 0, void 0, function* () {
      t(3, s.muted = !0, s), t(3, s.playsInline = !0, s), t(3, s.controls = !1, s), s.setAttribute("muted", ""), yield s.play(), s.pause();
    });
  }
  function c(_) {
    pc[_ ? "unshift" : "push"](() => {
      s = _, t(3, s);
    });
  }
  return i.$$set = (_) => {
    "type" in _ && t(0, l = _.type), "selected" in _ && t(1, o = _.selected), "value" in _ && t(2, r = _.value), "loop" in _ && t(5, a = _.loop);
  }, [l, o, r, s, f, a, c];
}
class Yc extends hc {
  constructor(e) {
    super(), bc(this, e, Tc, Ec, vc, { type: 0, selected: 1, value: 2, loop: 5 });
  }
}
const {
  SvelteComponent: yc,
  add_flush_callback: Ac,
  assign: Sc,
  bind: Cc,
  binding_callbacks: Lc,
  create_component: ln,
  destroy_component: on,
  detach: Rc,
  flush: x,
  get_spread_object: Dc,
  get_spread_update: Ic,
  init: Oc,
  insert: Nc,
  mount_component: rn,
  safe_not_equal: Mc,
  space: Pc,
  transition_in: sn,
  transition_out: an
} = window.__gradio__svelte__internal;
function Uc(i) {
  let e, t;
  return e = new Vs({
    props: {
      i18n: (
        /*gradio*/
        i[14].i18n
      ),
      type: "video"
    }
  }), {
    c() {
      ln(e.$$.fragment);
    },
    m(n, l) {
      rn(e, n, l), t = !0;
    },
    p(n, l) {
      const o = {};
      l & /*gradio*/
      16384 && (o.i18n = /*gradio*/
      n[14].i18n), e.$set(o);
    },
    i(n) {
      t || (sn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      an(e.$$.fragment, n), t = !1;
    },
    d(n) {
      on(e, n);
    }
  };
}
function Fc(i) {
  let e, t, n, l, o;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        i[14].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      i[14].i18n
    ) },
    /*loading_status*/
    i[7]
  ];
  let a = {};
  for (let c = 0; c < r.length; c += 1)
    a = Sc(a, r[c]);
  e = new Da({ props: a }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    i[17]
  );
  function s(c) {
    i[19](c);
  }
  let f = {
    label: (
      /*label*/
      i[4]
    ),
    show_label: (
      /*show_label*/
      i[6]
    ),
    active_source: "webcam",
    include_audio: !1,
    root: (
      /*root*/
      i[5]
    ),
    server: (
      /*server*/
      i[10]
    ),
    rtc_configuration: (
      /*rtc_configuration*/
      i[15]
    ),
    time_limit: (
      /*time_limit*/
      i[16]
    ),
    i18n: (
      /*gradio*/
      i[14].i18n
    ),
    stream_handler: (
      /*func*/
      i[18]
    ),
    $$slots: { default: [Uc] },
    $$scope: { ctx: i }
  };
  return (
    /*value*/
    i[0] !== void 0 && (f.value = /*value*/
    i[0]), n = new mc({ props: f }), Lc.push(() => Cc(n, "value", s)), n.$on(
      "clear",
      /*clear_handler*/
      i[20]
    ), n.$on(
      "play",
      /*play_handler*/
      i[21]
    ), n.$on(
      "pause",
      /*pause_handler*/
      i[22]
    ), n.$on(
      "upload",
      /*upload_handler*/
      i[23]
    ), n.$on(
      "stop",
      /*stop_handler*/
      i[24]
    ), n.$on(
      "end",
      /*end_handler*/
      i[25]
    ), n.$on(
      "start_recording",
      /*start_recording_handler*/
      i[26]
    ), n.$on(
      "stop_recording",
      /*stop_recording_handler*/
      i[27]
    ), n.$on(
      "tick",
      /*tick_handler*/
      i[28]
    ), n.$on(
      "error",
      /*error_handler*/
      i[29]
    ), {
      c() {
        ln(e.$$.fragment), t = Pc(), ln(n.$$.fragment);
      },
      m(c, _) {
        rn(e, c, _), Nc(c, t, _), rn(n, c, _), o = !0;
      },
      p(c, _) {
        const d = _ & /*gradio, loading_status*/
        16512 ? Ic(r, [
          _ & /*gradio*/
          16384 && {
            autoscroll: (
              /*gradio*/
              c[14].autoscroll
            )
          },
          _ & /*gradio*/
          16384 && { i18n: (
            /*gradio*/
            c[14].i18n
          ) },
          _ & /*loading_status*/
          128 && Dc(
            /*loading_status*/
            c[7]
          )
        ]) : {};
        e.$set(d);
        const m = {};
        _ & /*label*/
        16 && (m.label = /*label*/
        c[4]), _ & /*show_label*/
        64 && (m.show_label = /*show_label*/
        c[6]), _ & /*root*/
        32 && (m.root = /*root*/
        c[5]), _ & /*server*/
        1024 && (m.server = /*server*/
        c[10]), _ & /*rtc_configuration*/
        32768 && (m.rtc_configuration = /*rtc_configuration*/
        c[15]), _ & /*time_limit*/
        65536 && (m.time_limit = /*time_limit*/
        c[16]), _ & /*gradio*/
        16384 && (m.i18n = /*gradio*/
        c[14].i18n), _ & /*gradio*/
        16384 && (m.stream_handler = /*func*/
        c[18]), _ & /*$$scope, gradio*/
        1073758208 && (m.$$scope = { dirty: _, ctx: c }), !l && _ & /*value*/
        1 && (l = !0, m.value = /*value*/
        c[0], Ac(() => l = !1)), n.$set(m);
      },
      i(c) {
        o || (sn(e.$$.fragment, c), sn(n.$$.fragment, c), o = !0);
      },
      o(c) {
        an(e.$$.fragment, c), an(n.$$.fragment, c), o = !1;
      },
      d(c) {
        c && Rc(t), on(e, c), on(n, c);
      }
    }
  );
}
function zc(i) {
  let e, t;
  return e = new jo({
    props: {
      visible: (
        /*visible*/
        i[3]
      ),
      variant: "solid",
      border_mode: "base",
      padding: !1,
      elem_id: (
        /*elem_id*/
        i[1]
      ),
      elem_classes: (
        /*elem_classes*/
        i[2]
      ),
      height: (
        /*height*/
        i[8]
      ),
      width: (
        /*width*/
        i[9]
      ),
      container: (
        /*container*/
        i[11]
      ),
      scale: (
        /*scale*/
        i[12]
      ),
      min_width: (
        /*min_width*/
        i[13]
      ),
      allow_overflow: !1,
      $$slots: { default: [Fc] },
      $$scope: { ctx: i }
    }
  }), {
    c() {
      ln(e.$$.fragment);
    },
    m(n, l) {
      rn(e, n, l), t = !0;
    },
    p(n, [l]) {
      const o = {};
      l & /*visible*/
      8 && (o.visible = /*visible*/
      n[3]), l & /*elem_id*/
      2 && (o.elem_id = /*elem_id*/
      n[1]), l & /*elem_classes*/
      4 && (o.elem_classes = /*elem_classes*/
      n[2]), l & /*height*/
      256 && (o.height = /*height*/
      n[8]), l & /*width*/
      512 && (o.width = /*width*/
      n[9]), l & /*container*/
      2048 && (o.container = /*container*/
      n[11]), l & /*scale*/
      4096 && (o.scale = /*scale*/
      n[12]), l & /*min_width*/
      8192 && (o.min_width = /*min_width*/
      n[13]), l & /*$$scope, label, show_label, root, server, rtc_configuration, time_limit, gradio, value, loading_status*/
      1073857777 && (o.$$scope = { dirty: l, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (sn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      an(e.$$.fragment, n), t = !1;
    },
    d(n) {
      on(e, n);
    }
  };
}
function qc(i, e, t) {
  let { elem_id: n = "" } = e, { elem_classes: l = [] } = e, { visible: o = !0 } = e, { value: r } = e, { label: a } = e, { root: s } = e, { show_label: f } = e, { loading_status: c } = e, { height: _ } = e, { width: d } = e, { server: m } = e, { container: w = !1 } = e, { scale: E = null } = e, { min_width: k = void 0 } = e, { gradio: p } = e, { rtc_configuration: L } = e, { time_limit: b = null } = e;
  const h = () => p.dispatch("clear_status", c), N = (...y) => p.client.stream(...y);
  function M(y) {
    r = y, t(0, r);
  }
  const H = () => p.dispatch("clear"), j = () => p.dispatch("play"), S = () => p.dispatch("pause"), ce = () => p.dispatch("upload"), G = () => p.dispatch("stop"), re = () => p.dispatch("end"), De = () => p.dispatch("start_recording"), C = () => p.dispatch("stop_recording"), V = () => p.dispatch("tick"), P = ({ detail: y }) => p.dispatch("error", y);
  return i.$$set = (y) => {
    "elem_id" in y && t(1, n = y.elem_id), "elem_classes" in y && t(2, l = y.elem_classes), "visible" in y && t(3, o = y.visible), "value" in y && t(0, r = y.value), "label" in y && t(4, a = y.label), "root" in y && t(5, s = y.root), "show_label" in y && t(6, f = y.show_label), "loading_status" in y && t(7, c = y.loading_status), "height" in y && t(8, _ = y.height), "width" in y && t(9, d = y.width), "server" in y && t(10, m = y.server), "container" in y && t(11, w = y.container), "scale" in y && t(12, E = y.scale), "min_width" in y && t(13, k = y.min_width), "gradio" in y && t(14, p = y.gradio), "rtc_configuration" in y && t(15, L = y.rtc_configuration), "time_limit" in y && t(16, b = y.time_limit);
  }, i.$$.update = () => {
    i.$$.dirty & /*value*/
    1 && console.log("value", r);
  }, [
    r,
    n,
    l,
    o,
    a,
    s,
    f,
    c,
    _,
    d,
    m,
    w,
    E,
    k,
    p,
    L,
    b,
    h,
    N,
    M,
    H,
    j,
    S,
    ce,
    G,
    re,
    De,
    C,
    V,
    P
  ];
}
class Xc extends yc {
  constructor(e) {
    super(), Oc(this, e, qc, zc, Mc, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      label: 4,
      root: 5,
      show_label: 6,
      loading_status: 7,
      height: 8,
      width: 9,
      server: 10,
      container: 11,
      scale: 12,
      min_width: 13,
      gradio: 14,
      rtc_configuration: 15,
      time_limit: 16
    });
  }
  get elem_id() {
    return this.$$.ctx[1];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), x();
  }
  get elem_classes() {
    return this.$$.ctx[2];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), x();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(e) {
    this.$$set({ visible: e }), x();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), x();
  }
  get label() {
    return this.$$.ctx[4];
  }
  set label(e) {
    this.$$set({ label: e }), x();
  }
  get root() {
    return this.$$.ctx[5];
  }
  set root(e) {
    this.$$set({ root: e }), x();
  }
  get show_label() {
    return this.$$.ctx[6];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), x();
  }
  get loading_status() {
    return this.$$.ctx[7];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), x();
  }
  get height() {
    return this.$$.ctx[8];
  }
  set height(e) {
    this.$$set({ height: e }), x();
  }
  get width() {
    return this.$$.ctx[9];
  }
  set width(e) {
    this.$$set({ width: e }), x();
  }
  get server() {
    return this.$$.ctx[10];
  }
  set server(e) {
    this.$$set({ server: e }), x();
  }
  get container() {
    return this.$$.ctx[11];
  }
  set container(e) {
    this.$$set({ container: e }), x();
  }
  get scale() {
    return this.$$.ctx[12];
  }
  set scale(e) {
    this.$$set({ scale: e }), x();
  }
  get min_width() {
    return this.$$.ctx[13];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), x();
  }
  get gradio() {
    return this.$$.ctx[14];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), x();
  }
  get rtc_configuration() {
    return this.$$.ctx[15];
  }
  set rtc_configuration(e) {
    this.$$set({ rtc_configuration: e }), x();
  }
  get time_limit() {
    return this.$$.ctx[16];
  }
  set time_limit(e) {
    this.$$set({ time_limit: e }), x();
  }
}
export {
  Yc as BaseExample,
  mc as BaseInteractiveVideo,
  Xc as default,
  Gc as loaded,
  jc as playable,
  Hc as prettyBytes
};
