const {
  SvelteComponent: dr,
  assign: mr,
  create_slot: hr,
  detach: gr,
  element: pr,
  get_all_dirty_from_scope: br,
  get_slot_changes: wr,
  get_spread_update: vr,
  init: kr,
  insert: yr,
  safe_not_equal: Er,
  set_dynamic_element_data: Si,
  set_style: Ce,
  toggle_class: nt,
  transition_in: oa,
  transition_out: aa,
  update_slot_base: Tr
} = window.__gradio__svelte__internal;
function Ar(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = hr(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let r = 0; r < s.length; r += 1)
    f = mr(f, s[r]);
  return {
    c() {
      e = pr(
        /*tag*/
        l[14]
      ), o && o.c(), Si(
        /*tag*/
        l[14]
      )(e, f), nt(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), nt(
        e,
        "padded",
        /*padding*/
        l[6]
      ), nt(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), nt(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), nt(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), Ce(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), Ce(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), Ce(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), Ce(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), Ce(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), Ce(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), Ce(e, "border-width", "var(--block-border-width)");
    },
    m(r, a) {
      yr(r, e, a), o && o.m(e, null), n = !0;
    },
    p(r, a) {
      o && o.p && (!n || a & /*$$scope*/
      131072) && Tr(
        o,
        i,
        r,
        /*$$scope*/
        r[17],
        n ? wr(
          i,
          /*$$scope*/
          r[17],
          a,
          null
        ) : br(
          /*$$scope*/
          r[17]
        ),
        null
      ), Si(
        /*tag*/
        r[14]
      )(e, f = vr(s, [
        (!n || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!n || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!n || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), nt(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), nt(
        e,
        "padded",
        /*padding*/
        r[6]
      ), nt(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), nt(
        e,
        "border_contrast",
        /*border_mode*/
        r[5] === "contrast"
      ), nt(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), a & /*height*/
      1 && Ce(
        e,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), a & /*width*/
      2 && Ce(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), a & /*variant*/
      16 && Ce(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), a & /*allow_overflow*/
      2048 && Ce(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && Ce(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), a & /*min_width*/
      8192 && Ce(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      n || (oa(o, r), n = !0);
    },
    o(r) {
      aa(o, r), n = !1;
    },
    d(r) {
      r && gr(e), o && o.d(r);
    }
  };
}
function Sr(l) {
  let e, t = (
    /*tag*/
    l[14] && Ar(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (oa(t, n), e = !0);
    },
    o(n) {
      aa(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Cr(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: r = [] } = e, { variant: a = "solid" } = e, { border_mode: u = "base" } = e, { padding: c = !0 } = e, { type: _ = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: m = !1 } = e, { container: g = !0 } = e, { visible: y = !0 } = e, { allow_overflow: E = !0 } = e, { scale: k = null } = e, { min_width: w = 0 } = e, p = _ === "fieldset" ? "fieldset" : "div";
  const R = (b) => {
    if (b !== void 0) {
      if (typeof b == "number")
        return b + "px";
      if (typeof b == "string")
        return b;
    }
  };
  return l.$$set = (b) => {
    "height" in b && t(0, o = b.height), "width" in b && t(1, s = b.width), "elem_id" in b && t(2, f = b.elem_id), "elem_classes" in b && t(3, r = b.elem_classes), "variant" in b && t(4, a = b.variant), "border_mode" in b && t(5, u = b.border_mode), "padding" in b && t(6, c = b.padding), "type" in b && t(16, _ = b.type), "test_id" in b && t(7, d = b.test_id), "explicit_call" in b && t(8, m = b.explicit_call), "container" in b && t(9, g = b.container), "visible" in b && t(10, y = b.visible), "allow_overflow" in b && t(11, E = b.allow_overflow), "scale" in b && t(12, k = b.scale), "min_width" in b && t(13, w = b.min_width), "$$scope" in b && t(17, i = b.$$scope);
  }, [
    o,
    s,
    f,
    r,
    a,
    u,
    c,
    d,
    m,
    g,
    y,
    E,
    k,
    w,
    p,
    R,
    _,
    i,
    n
  ];
}
class Lr extends dr {
  constructor(e) {
    super(), kr(this, e, Cr, Sr, Er, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Rr,
  append: fl,
  attr: An,
  create_component: Dr,
  destroy_component: Or,
  detach: Ir,
  element: Ci,
  init: Mr,
  insert: Nr,
  mount_component: Pr,
  safe_not_equal: Fr,
  set_data: zr,
  space: Ur,
  text: qr,
  toggle_class: pt,
  transition_in: Br,
  transition_out: Hr
} = window.__gradio__svelte__internal;
function jr(l) {
  let e, t, n, i, o, s;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = Ci("label"), t = Ci("span"), Dr(n.$$.fragment), i = Ur(), o = qr(
        /*label*/
        l[0]
      ), An(t, "class", "svelte-9gxdi0"), An(e, "for", ""), An(e, "data-testid", "block-label"), An(e, "class", "svelte-9gxdi0"), pt(e, "hide", !/*show_label*/
      l[2]), pt(e, "sr-only", !/*show_label*/
      l[2]), pt(
        e,
        "float",
        /*float*/
        l[4]
      ), pt(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, r) {
      Nr(f, e, r), fl(e, t), Pr(n, t, null), fl(e, i), fl(e, o), s = !0;
    },
    p(f, [r]) {
      (!s || r & /*label*/
      1) && zr(
        o,
        /*label*/
        f[0]
      ), (!s || r & /*show_label*/
      4) && pt(e, "hide", !/*show_label*/
      f[2]), (!s || r & /*show_label*/
      4) && pt(e, "sr-only", !/*show_label*/
      f[2]), (!s || r & /*float*/
      16) && pt(
        e,
        "float",
        /*float*/
        f[4]
      ), (!s || r & /*disable*/
      8) && pt(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      s || (Br(n.$$.fragment, f), s = !0);
    },
    o(f) {
      Hr(n.$$.fragment, f), s = !1;
    },
    d(f) {
      f && Ir(e), Or(n);
    }
  };
}
function Wr(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: s = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (r) => {
    "label" in r && t(0, n = r.label), "Icon" in r && t(1, i = r.Icon), "show_label" in r && t(2, o = r.show_label), "disable" in r && t(3, s = r.disable), "float" in r && t(4, f = r.float);
  }, [n, i, o, s, f];
}
class ra extends Rr {
  constructor(e) {
    super(), Mr(this, e, Wr, jr, Fr, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Gr,
  append: Fl,
  attr: ht,
  bubble: Vr,
  create_component: Yr,
  destroy_component: Xr,
  detach: sa,
  element: zl,
  init: Zr,
  insert: fa,
  listen: Kr,
  mount_component: Jr,
  safe_not_equal: Qr,
  set_data: xr,
  set_style: Vt,
  space: $r,
  text: es,
  toggle_class: Ee,
  transition_in: ts,
  transition_out: ns
} = window.__gradio__svelte__internal;
function Li(l) {
  let e, t;
  return {
    c() {
      e = zl("span"), t = es(
        /*label*/
        l[1]
      ), ht(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      fa(n, e, i), Fl(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && xr(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && sa(e);
    }
  };
}
function ls(l) {
  let e, t, n, i, o, s, f, r = (
    /*show_label*/
    l[2] && Li(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = zl("button"), r && r.c(), t = $r(), n = zl("div"), Yr(i.$$.fragment), ht(n, "class", "svelte-1lrphxw"), Ee(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), Ee(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), Ee(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], ht(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), ht(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), ht(
        e,
        "title",
        /*label*/
        l[1]
      ), ht(e, "class", "svelte-1lrphxw"), Ee(
        e,
        "pending",
        /*pending*/
        l[3]
      ), Ee(
        e,
        "padded",
        /*padded*/
        l[5]
      ), Ee(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), Ee(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Vt(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Vt(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Vt(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(a, u) {
      fa(a, e, u), r && r.m(e, null), Fl(e, t), Fl(e, n), Jr(i, n, null), o = !0, s || (f = Kr(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(a, [u]) {
      /*show_label*/
      a[2] ? r ? r.p(a, u) : (r = Li(a), r.c(), r.m(e, t)) : r && (r.d(1), r = null), (!o || u & /*size*/
      16) && Ee(
        n,
        "small",
        /*size*/
        a[4] === "small"
      ), (!o || u & /*size*/
      16) && Ee(
        n,
        "large",
        /*size*/
        a[4] === "large"
      ), (!o || u & /*size*/
      16) && Ee(
        n,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!o || u & /*label*/
      2) && ht(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!o || u & /*hasPopup*/
      256) && ht(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!o || u & /*label*/
      2) && ht(
        e,
        "title",
        /*label*/
        a[1]
      ), (!o || u & /*pending*/
      8) && Ee(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!o || u & /*padded*/
      32) && Ee(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!o || u & /*highlight*/
      64) && Ee(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!o || u & /*transparent*/
      512) && Ee(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), u & /*disabled, _color*/
      4224 && Vt(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Vt(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), u & /*offset*/
      2048 && Vt(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      o || (ts(i.$$.fragment, a), o = !0);
    },
    o(a) {
      ns(i.$$.fragment, a), o = !1;
    },
    d(a) {
      a && sa(e), r && r.d(), Xr(i), s = !1, f();
    }
  };
}
function is(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: s = !1 } = e, { pending: f = !1 } = e, { size: r = "small" } = e, { padded: a = !0 } = e, { highlight: u = !1 } = e, { disabled: c = !1 } = e, { hasPopup: _ = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: g = "var(--background-fill-primary)" } = e, { offset: y = 0 } = e;
  function E(k) {
    Vr.call(this, l, k);
  }
  return l.$$set = (k) => {
    "Icon" in k && t(0, i = k.Icon), "label" in k && t(1, o = k.label), "show_label" in k && t(2, s = k.show_label), "pending" in k && t(3, f = k.pending), "size" in k && t(4, r = k.size), "padded" in k && t(5, a = k.padded), "highlight" in k && t(6, u = k.highlight), "disabled" in k && t(7, c = k.disabled), "hasPopup" in k && t(8, _ = k.hasPopup), "color" in k && t(13, d = k.color), "transparent" in k && t(9, m = k.transparent), "background" in k && t(10, g = k.background), "offset" in k && t(11, y = k.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : d);
  }, [
    i,
    o,
    s,
    f,
    r,
    a,
    u,
    c,
    _,
    m,
    g,
    y,
    n,
    d,
    E
  ];
}
class Bt extends Gr {
  constructor(e) {
    super(), Zr(this, e, is, ls, Qr, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: os,
  append: as,
  attr: ul,
  binding_callbacks: rs,
  create_slot: ss,
  detach: fs,
  element: Ri,
  get_all_dirty_from_scope: us,
  get_slot_changes: cs,
  init: _s,
  insert: ds,
  safe_not_equal: ms,
  toggle_class: bt,
  transition_in: hs,
  transition_out: gs,
  update_slot_base: ps
} = window.__gradio__svelte__internal;
function bs(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = ss(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Ri("div"), t = Ri("div"), o && o.c(), ul(t, "class", "icon svelte-3w3rth"), ul(e, "class", "empty svelte-3w3rth"), ul(e, "aria-label", "Empty value"), bt(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), bt(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), bt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), bt(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(s, f) {
      ds(s, e, f), as(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(s, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && ps(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        n ? cs(
          i,
          /*$$scope*/
          s[4],
          f,
          null
        ) : us(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && bt(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!n || f & /*size*/
      1) && bt(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && bt(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!n || f & /*parent_height*/
      8) && bt(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      n || (hs(o, s), n = !0);
    },
    o(s) {
      gs(o, s), n = !1;
    },
    d(s) {
      s && fs(e), o && o.d(s), l[6](null);
    }
  };
}
function ws(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: s = "small" } = e, { unpadded_box: f = !1 } = e, r;
  function a(c) {
    var _;
    if (!c) return !1;
    const { height: d } = c.getBoundingClientRect(), { height: m } = ((_ = c.parentElement) === null || _ === void 0 ? void 0 : _.getBoundingClientRect()) || { height: d };
    return d > m + 2;
  }
  function u(c) {
    rs[c ? "unshift" : "push"](() => {
      r = c, t(2, r);
    });
  }
  return l.$$set = (c) => {
    "size" in c && t(0, s = c.size), "unpadded_box" in c && t(1, f = c.unpadded_box), "$$scope" in c && t(4, o = c.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = a(r));
  }, [s, f, r, n, o, i, u];
}
class vs extends os {
  constructor(e) {
    super(), _s(this, e, ws, bs, ms, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: ks,
  append: cl,
  attr: Ve,
  detach: ys,
  init: Es,
  insert: Ts,
  noop: _l,
  safe_not_equal: As,
  set_style: lt,
  svg_element: Sn
} = window.__gradio__svelte__internal;
function Ss(l) {
  let e, t, n, i;
  return {
    c() {
      e = Sn("svg"), t = Sn("g"), n = Sn("path"), i = Sn("path"), Ve(n, "d", "M18,6L6.087,17.913"), lt(n, "fill", "none"), lt(n, "fill-rule", "nonzero"), lt(n, "stroke-width", "2px"), Ve(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Ve(i, "d", "M4.364,4.364L19.636,19.636"), lt(i, "fill", "none"), lt(i, "fill-rule", "nonzero"), lt(i, "stroke-width", "2px"), Ve(e, "width", "100%"), Ve(e, "height", "100%"), Ve(e, "viewBox", "0 0 24 24"), Ve(e, "version", "1.1"), Ve(e, "xmlns", "http://www.w3.org/2000/svg"), Ve(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Ve(e, "xml:space", "preserve"), Ve(e, "stroke", "currentColor"), lt(e, "fill-rule", "evenodd"), lt(e, "clip-rule", "evenodd"), lt(e, "stroke-linecap", "round"), lt(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      Ts(o, e, s), cl(e, t), cl(t, n), cl(e, i);
    },
    p: _l,
    i: _l,
    o: _l,
    d(o) {
      o && ys(e);
    }
  };
}
class ua extends ks {
  constructor(e) {
    super(), Es(this, e, null, Ss, As, {});
  }
}
const {
  SvelteComponent: Cs,
  append: Ls,
  attr: tn,
  detach: Rs,
  init: Ds,
  insert: Os,
  noop: dl,
  safe_not_equal: Is,
  svg_element: Di
} = window.__gradio__svelte__internal;
function Ms(l) {
  let e, t;
  return {
    c() {
      e = Di("svg"), t = Di("path"), tn(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), tn(t, "fill", "currentColor"), tn(e, "id", "icon"), tn(e, "xmlns", "http://www.w3.org/2000/svg"), tn(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      Os(n, e, i), Ls(e, t);
    },
    p: dl,
    i: dl,
    o: dl,
    d(n) {
      n && Rs(e);
    }
  };
}
class Ns extends Cs {
  constructor(e) {
    super(), Ds(this, e, null, Ms, Is, {});
  }
}
const {
  SvelteComponent: Ps,
  append: Fs,
  attr: Yt,
  detach: zs,
  init: Us,
  insert: qs,
  noop: ml,
  safe_not_equal: Bs,
  svg_element: Oi
} = window.__gradio__svelte__internal;
function Hs(l) {
  let e, t;
  return {
    c() {
      e = Oi("svg"), t = Oi("path"), Yt(t, "fill", "currentColor"), Yt(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Yt(e, "xmlns", "http://www.w3.org/2000/svg"), Yt(e, "width", "100%"), Yt(e, "height", "100%"), Yt(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      qs(n, e, i), Fs(e, t);
    },
    p: ml,
    i: ml,
    o: ml,
    d(n) {
      n && zs(e);
    }
  };
}
class ca extends Ps {
  constructor(e) {
    super(), Us(this, e, null, Hs, Bs, {});
  }
}
const {
  SvelteComponent: js,
  append: Ws,
  attr: Ye,
  detach: Gs,
  init: Vs,
  insert: Ys,
  noop: hl,
  safe_not_equal: Xs,
  svg_element: Ii
} = window.__gradio__svelte__internal;
function Zs(l) {
  let e, t;
  return {
    c() {
      e = Ii("svg"), t = Ii("path"), Ye(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), Ye(e, "xmlns", "http://www.w3.org/2000/svg"), Ye(e, "width", "100%"), Ye(e, "height", "100%"), Ye(e, "viewBox", "0 0 24 24"), Ye(e, "fill", "none"), Ye(e, "stroke", "currentColor"), Ye(e, "stroke-width", "1.5"), Ye(e, "stroke-linecap", "round"), Ye(e, "stroke-linejoin", "round"), Ye(e, "class", "feather feather-edit-2");
    },
    m(n, i) {
      Ys(n, e, i), Ws(e, t);
    },
    p: hl,
    i: hl,
    o: hl,
    d(n) {
      n && Gs(e);
    }
  };
}
class Ks extends js {
  constructor(e) {
    super(), Vs(this, e, null, Zs, Xs, {});
  }
}
const {
  SvelteComponent: Js,
  append: Mi,
  attr: Ne,
  detach: Qs,
  init: xs,
  insert: $s,
  noop: gl,
  safe_not_equal: ef,
  svg_element: pl
} = window.__gradio__svelte__internal;
function tf(l) {
  let e, t, n;
  return {
    c() {
      e = pl("svg"), t = pl("path"), n = pl("polyline"), Ne(t, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), Ne(n, "points", "13 2 13 9 20 9"), Ne(e, "xmlns", "http://www.w3.org/2000/svg"), Ne(e, "width", "100%"), Ne(e, "height", "100%"), Ne(e, "viewBox", "0 0 24 24"), Ne(e, "fill", "none"), Ne(e, "stroke", "currentColor"), Ne(e, "stroke-width", "1.5"), Ne(e, "stroke-linecap", "round"), Ne(e, "stroke-linejoin", "round"), Ne(e, "class", "feather feather-file");
    },
    m(i, o) {
      $s(i, e, o), Mi(e, t), Mi(e, n);
    },
    p: gl,
    i: gl,
    o: gl,
    d(i) {
      i && Qs(e);
    }
  };
}
let nf = class extends Js {
  constructor(e) {
    super(), xs(this, e, null, tf, ef, {});
  }
};
const {
  SvelteComponent: lf,
  append: bl,
  attr: le,
  detach: of,
  init: af,
  insert: rf,
  noop: wl,
  safe_not_equal: sf,
  svg_element: Cn
} = window.__gradio__svelte__internal;
function ff(l) {
  let e, t, n, i;
  return {
    c() {
      e = Cn("svg"), t = Cn("rect"), n = Cn("circle"), i = Cn("polyline"), le(t, "x", "3"), le(t, "y", "3"), le(t, "width", "18"), le(t, "height", "18"), le(t, "rx", "2"), le(t, "ry", "2"), le(n, "cx", "8.5"), le(n, "cy", "8.5"), le(n, "r", "1.5"), le(i, "points", "21 15 16 10 5 21"), le(e, "xmlns", "http://www.w3.org/2000/svg"), le(e, "width", "100%"), le(e, "height", "100%"), le(e, "viewBox", "0 0 24 24"), le(e, "fill", "none"), le(e, "stroke", "currentColor"), le(e, "stroke-width", "1.5"), le(e, "stroke-linecap", "round"), le(e, "stroke-linejoin", "round"), le(e, "class", "feather feather-image");
    },
    m(o, s) {
      rf(o, e, s), bl(e, t), bl(e, n), bl(e, i);
    },
    p: wl,
    i: wl,
    o: wl,
    d(o) {
      o && of(e);
    }
  };
}
let _a = class extends lf {
  constructor(e) {
    super(), af(this, e, null, ff, sf, {});
  }
};
const {
  SvelteComponent: uf,
  append: cf,
  attr: Ln,
  detach: _f,
  init: df,
  insert: mf,
  noop: vl,
  safe_not_equal: hf,
  svg_element: Ni
} = window.__gradio__svelte__internal;
function gf(l) {
  let e, t;
  return {
    c() {
      e = Ni("svg"), t = Ni("path"), Ln(t, "fill", "currentColor"), Ln(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a4 4 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2zm2.245 2.096L16 4.25q0-.078-.005-.154M13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5M15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3zm0 11a3 3 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A3 3 0 0 1 20 23zm5-7a1 1 0 1 1 0-2 1 1 0 0 1 0 2"), Ln(e, "xmlns", "http://www.w3.org/2000/svg"), Ln(e, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      mf(n, e, i), cf(e, t);
    },
    p: vl,
    i: vl,
    o: vl,
    d(n) {
      n && _f(e);
    }
  };
}
class pf extends uf {
  constructor(e) {
    super(), df(this, e, null, gf, hf, {});
  }
}
const {
  SvelteComponent: bf,
  append: Pi,
  attr: Pe,
  detach: wf,
  init: vf,
  insert: kf,
  noop: kl,
  safe_not_equal: yf,
  svg_element: yl
} = window.__gradio__svelte__internal;
function Ef(l) {
  let e, t, n;
  return {
    c() {
      e = yl("svg"), t = yl("polyline"), n = yl("path"), Pe(t, "points", "1 4 1 10 7 10"), Pe(n, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), Pe(e, "xmlns", "http://www.w3.org/2000/svg"), Pe(e, "width", "100%"), Pe(e, "height", "100%"), Pe(e, "viewBox", "0 0 24 24"), Pe(e, "fill", "none"), Pe(e, "stroke", "currentColor"), Pe(e, "stroke-width", "2"), Pe(e, "stroke-linecap", "round"), Pe(e, "stroke-linejoin", "round"), Pe(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      kf(i, e, o), Pi(e, t), Pi(e, n);
    },
    p: kl,
    i: kl,
    o: kl,
    d(i) {
      i && wf(e);
    }
  };
}
class Tf extends bf {
  constructor(e) {
    super(), vf(this, e, null, Ef, yf, {});
  }
}
const {
  SvelteComponent: Af,
  append: El,
  attr: he,
  detach: Sf,
  init: Cf,
  insert: Lf,
  noop: Tl,
  safe_not_equal: Rf,
  svg_element: Rn
} = window.__gradio__svelte__internal;
function Df(l) {
  let e, t, n, i;
  return {
    c() {
      e = Rn("svg"), t = Rn("path"), n = Rn("polyline"), i = Rn("line"), he(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), he(n, "points", "17 8 12 3 7 8"), he(i, "x1", "12"), he(i, "y1", "3"), he(i, "x2", "12"), he(i, "y2", "15"), he(e, "xmlns", "http://www.w3.org/2000/svg"), he(e, "width", "90%"), he(e, "height", "90%"), he(e, "viewBox", "0 0 24 24"), he(e, "fill", "none"), he(e, "stroke", "currentColor"), he(e, "stroke-width", "2"), he(e, "stroke-linecap", "round"), he(e, "stroke-linejoin", "round"), he(e, "class", "feather feather-upload");
    },
    m(o, s) {
      Lf(o, e, s), El(e, t), El(e, n), El(e, i);
    },
    p: Tl,
    i: Tl,
    o: Tl,
    d(o) {
      o && Sf(e);
    }
  };
}
let Of = class extends Af {
  constructor(e) {
    super(), Cf(this, e, null, Df, Rf, {});
  }
};
const If = [
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
If.reduce((l, { color: e, primary: t, secondary: n }) => ({
  ...l,
  [e]: {
    primary: Fi[e][t],
    secondary: Fi[e][n]
  }
}), {});
class zn extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
async function Mf(l, e) {
  var r;
  if (window.__gradio_space__ == null)
    throw new zn("Must be on Spaces to share.");
  let t, n, i;
  {
    let a;
    if (typeof l == "object" && l.url)
      a = l.url;
    else if (typeof l == "string")
      a = l;
    else
      throw new Error("Invalid data format for URL type");
    const u = await fetch(a);
    t = await u.blob(), n = u.headers.get("content-type") || "", i = u.headers.get("content-disposition") || "";
  }
  const o = new File([t], i, { type: n }), s = await fetch("https://huggingface.co/uploads", {
    method: "POST",
    body: o,
    headers: {
      "Content-Type": o.type,
      "X-Requested-With": "XMLHttpRequest"
    }
  });
  if (!s.ok) {
    if ((r = s.headers.get("content-type")) != null && r.includes("application/json")) {
      const a = await s.json();
      throw new zn(`Upload failed: ${a.error}`);
    }
    throw new zn("Upload failed.");
  }
  return await s.text();
}
const {
  SvelteComponent: Nf,
  create_component: Pf,
  destroy_component: Ff,
  init: zf,
  mount_component: Uf,
  safe_not_equal: qf,
  transition_in: Bf,
  transition_out: Hf
} = window.__gradio__svelte__internal, { createEventDispatcher: jf } = window.__gradio__svelte__internal;
function Wf(l) {
  let e, t;
  return e = new Bt({
    props: {
      Icon: Ns,
      label: (
        /*i18n*/
        l[2]("common.share")
      ),
      pending: (
        /*pending*/
        l[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[5]
  ), {
    c() {
      Pf(e.$$.fragment);
    },
    m(n, i) {
      Uf(e, n, i), t = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      t || (Bf(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Hf(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ff(e, n);
    }
  };
}
function Gf(l, e, t) {
  const n = jf();
  let { formatter: i } = e, { value: o } = e, { i18n: s } = e, f = !1;
  const r = async () => {
    try {
      t(3, f = !0);
      const a = await i(o);
      n("share", { description: a });
    } catch (a) {
      console.error(a);
      let u = a instanceof zn ? a.message : "Share failed.";
      n("error", u);
    } finally {
      t(3, f = !1);
    }
  };
  return l.$$set = (a) => {
    "formatter" in a && t(0, i = a.formatter), "value" in a && t(1, o = a.value), "i18n" in a && t(2, s = a.i18n);
  }, [i, o, s, f, n, r];
}
class Vf extends Nf {
  constructor(e) {
    super(), zf(this, e, Gf, Wf, qf, { formatter: 0, value: 1, i18n: 2 });
  }
}
const {
  SvelteComponent: Yf,
  append: Ot,
  attr: Ul,
  check_outros: Xf,
  create_component: da,
  destroy_component: ma,
  detach: Un,
  element: ql,
  group_outros: Zf,
  init: Kf,
  insert: qn,
  mount_component: ha,
  safe_not_equal: Jf,
  set_data: Bl,
  space: Hl,
  text: fn,
  toggle_class: zi,
  transition_in: jn,
  transition_out: Wn
} = window.__gradio__svelte__internal;
function Qf(l) {
  let e, t;
  return e = new Of({}), {
    c() {
      da(e.$$.fragment);
    },
    m(n, i) {
      ha(e, n, i), t = !0;
    },
    i(n) {
      t || (jn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Wn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ma(e, n);
    }
  };
}
function xf(l) {
  let e, t;
  return e = new pf({}), {
    c() {
      da(e.$$.fragment);
    },
    m(n, i) {
      ha(e, n, i), t = !0;
    },
    i(n) {
      t || (jn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Wn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ma(e, n);
    }
  };
}
function Ui(l) {
  let e, t, n = (
    /*i18n*/
    l[1]("common.or") + ""
  ), i, o, s, f = (
    /*message*/
    (l[2] || /*i18n*/
    l[1]("upload_text.click_to_upload")) + ""
  ), r;
  return {
    c() {
      e = ql("span"), t = fn("- "), i = fn(n), o = fn(" -"), s = Hl(), r = fn(f), Ul(e, "class", "or svelte-kzcjhc");
    },
    m(a, u) {
      qn(a, e, u), Ot(e, t), Ot(e, i), Ot(e, o), qn(a, s, u), qn(a, r, u);
    },
    p(a, u) {
      u & /*i18n*/
      2 && n !== (n = /*i18n*/
      a[1]("common.or") + "") && Bl(i, n), u & /*message, i18n*/
      6 && f !== (f = /*message*/
      (a[2] || /*i18n*/
      a[1]("upload_text.click_to_upload")) + "") && Bl(r, f);
    },
    d(a) {
      a && (Un(e), Un(s), Un(r));
    }
  };
}
function $f(l) {
  let e, t, n, i, o, s = (
    /*i18n*/
    l[1](
      /*defs*/
      l[5][
        /*type*/
        l[0]
      ] || /*defs*/
      l[5].file
    ) + ""
  ), f, r, a;
  const u = [xf, Qf], c = [];
  function _(m, g) {
    return (
      /*type*/
      m[0] === "clipboard" ? 0 : 1
    );
  }
  n = _(l), i = c[n] = u[n](l);
  let d = (
    /*mode*/
    l[3] !== "short" && Ui(l)
  );
  return {
    c() {
      e = ql("div"), t = ql("span"), i.c(), o = Hl(), f = fn(s), r = Hl(), d && d.c(), Ul(t, "class", "icon-wrap svelte-kzcjhc"), zi(
        t,
        "hovered",
        /*hovered*/
        l[4]
      ), Ul(e, "class", "wrap svelte-kzcjhc");
    },
    m(m, g) {
      qn(m, e, g), Ot(e, t), c[n].m(t, null), Ot(e, o), Ot(e, f), Ot(e, r), d && d.m(e, null), a = !0;
    },
    p(m, [g]) {
      let y = n;
      n = _(m), n !== y && (Zf(), Wn(c[y], 1, 1, () => {
        c[y] = null;
      }), Xf(), i = c[n], i || (i = c[n] = u[n](m), i.c()), jn(i, 1), i.m(t, null)), (!a || g & /*hovered*/
      16) && zi(
        t,
        "hovered",
        /*hovered*/
        m[4]
      ), (!a || g & /*i18n, type*/
      3) && s !== (s = /*i18n*/
      m[1](
        /*defs*/
        m[5][
          /*type*/
          m[0]
        ] || /*defs*/
        m[5].file
      ) + "") && Bl(f, s), /*mode*/
      m[3] !== "short" ? d ? d.p(m, g) : (d = Ui(m), d.c(), d.m(e, null)) : d && (d.d(1), d = null);
    },
    i(m) {
      a || (jn(i), a = !0);
    },
    o(m) {
      Wn(i), a = !1;
    },
    d(m) {
      m && Un(e), c[n].d(), d && d.d();
    }
  };
}
function eu(l, e, t) {
  let { type: n = "file" } = e, { i18n: i } = e, { message: o = void 0 } = e, { mode: s = "full" } = e, { hovered: f = !1 } = e;
  const r = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv",
    gallery: "upload_text.drop_gallery",
    clipboard: "upload_text.paste_clipboard"
  };
  return l.$$set = (a) => {
    "type" in a && t(0, n = a.type), "i18n" in a && t(1, i = a.i18n), "message" in a && t(2, o = a.message), "mode" in a && t(3, s = a.mode), "hovered" in a && t(4, f = a.hovered);
  }, [n, i, o, s, f, r];
}
class tu extends Yf {
  constructor(e) {
    super(), Kf(this, e, eu, $f, Jf, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
var nu = Object.defineProperty, lu = (l, e, t) => e in l ? nu(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t, mt = (l, e, t) => (lu(l, typeof e != "symbol" ? e + "" : e, t), t), ga = (l, e, t) => {
  if (!e.has(l))
    throw TypeError("Cannot " + t);
}, nn = (l, e, t) => (ga(l, e, "read from private field"), t ? t.call(l) : e.get(l)), iu = (l, e, t) => {
  if (e.has(l))
    throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(l) : e.set(l, t);
}, ou = (l, e, t, n) => (ga(l, e, "write to private field"), e.set(l, t), t), wt;
new Intl.Collator(0, { numeric: 1 }).compare;
async function au(l, e) {
  return l.map(
    (t) => new ru({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class ru {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: f,
    alt_text: r
  }) {
    mt(this, "path"), mt(this, "url"), mt(this, "orig_name"), mt(this, "size"), mt(this, "blob"), mt(this, "is_stream"), mt(this, "mime_type"), mt(this, "alt_text"), mt(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = f, this.alt_text = r;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class Gd extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = { allowCR: !1 }) {
    super({
      transform: (t, n) => {
        for (t = nn(this, wt) + t; ; ) {
          const i = t.indexOf(`
`), o = e.allowCR ? t.indexOf("\r") : -1;
          if (o !== -1 && o !== t.length - 1 && (i === -1 || i - 1 > o)) {
            n.enqueue(t.slice(0, o)), t = t.slice(o + 1);
            continue;
          }
          if (i === -1)
            break;
          const s = t[i - 1] === "\r" ? i - 1 : i;
          n.enqueue(t.slice(0, s)), t = t.slice(i + 1);
        }
        ou(this, wt, t);
      },
      flush: (t) => {
        if (nn(this, wt) === "")
          return;
        const n = e.allowCR && nn(this, wt).endsWith("\r") ? nn(this, wt).slice(0, -1) : nn(this, wt);
        t.enqueue(n);
      }
    }), iu(this, wt, "");
  }
}
wt = /* @__PURE__ */ new WeakMap();
const {
  SvelteComponent: su,
  append: Ae,
  attr: Rt,
  detach: pa,
  element: Dt,
  init: fu,
  insert: ba,
  noop: qi,
  safe_not_equal: uu,
  set_data: Gn,
  set_style: Al,
  space: jl,
  text: Zt,
  toggle_class: Bi
} = window.__gradio__svelte__internal, { onMount: cu, createEventDispatcher: _u, onDestroy: du } = window.__gradio__svelte__internal;
function Hi(l) {
  let e, t, n, i, o = un(
    /*file_to_display*/
    l[2]
  ) + "", s, f, r, a, u = (
    /*file_to_display*/
    l[2].orig_name + ""
  ), c;
  return {
    c() {
      e = Dt("div"), t = Dt("span"), n = Dt("div"), i = Dt("progress"), s = Zt(o), r = jl(), a = Dt("span"), c = Zt(u), Al(i, "visibility", "hidden"), Al(i, "height", "0"), Al(i, "width", "0"), i.value = f = un(
        /*file_to_display*/
        l[2]
      ), Rt(i, "max", "100"), Rt(i, "class", "svelte-cr2edf"), Rt(n, "class", "progress-bar svelte-cr2edf"), Rt(a, "class", "file-name svelte-cr2edf"), Rt(e, "class", "file svelte-cr2edf");
    },
    m(_, d) {
      ba(_, e, d), Ae(e, t), Ae(t, n), Ae(n, i), Ae(i, s), Ae(e, r), Ae(e, a), Ae(a, c);
    },
    p(_, d) {
      d & /*file_to_display*/
      4 && o !== (o = un(
        /*file_to_display*/
        _[2]
      ) + "") && Gn(s, o), d & /*file_to_display*/
      4 && f !== (f = un(
        /*file_to_display*/
        _[2]
      )) && (i.value = f), d & /*file_to_display*/
      4 && u !== (u = /*file_to_display*/
      _[2].orig_name + "") && Gn(c, u);
    },
    d(_) {
      _ && pa(e);
    }
  };
}
function mu(l) {
  let e, t, n, i = (
    /*files_with_progress*/
    l[0].length + ""
  ), o, s, f = (
    /*files_with_progress*/
    l[0].length > 1 ? "files" : "file"
  ), r, a, u, c = (
    /*file_to_display*/
    l[2] && Hi(l)
  );
  return {
    c() {
      e = Dt("div"), t = Dt("span"), n = Zt("Uploading "), o = Zt(i), s = jl(), r = Zt(f), a = Zt("..."), u = jl(), c && c.c(), Rt(t, "class", "uploading svelte-cr2edf"), Rt(e, "class", "wrap svelte-cr2edf"), Bi(
        e,
        "progress",
        /*progress*/
        l[1]
      );
    },
    m(_, d) {
      ba(_, e, d), Ae(e, t), Ae(t, n), Ae(t, o), Ae(t, s), Ae(t, r), Ae(t, a), Ae(e, u), c && c.m(e, null);
    },
    p(_, [d]) {
      d & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      _[0].length + "") && Gn(o, i), d & /*files_with_progress*/
      1 && f !== (f = /*files_with_progress*/
      _[0].length > 1 ? "files" : "file") && Gn(r, f), /*file_to_display*/
      _[2] ? c ? c.p(_, d) : (c = Hi(_), c.c(), c.m(e, null)) : c && (c.d(1), c = null), d & /*progress*/
      2 && Bi(
        e,
        "progress",
        /*progress*/
        _[1]
      );
    },
    i: qi,
    o: qi,
    d(_) {
      _ && pa(e), c && c.d();
    }
  };
}
function un(l) {
  return l.progress * 100 / (l.size || 0) || 0;
}
function hu(l) {
  let e = 0;
  return l.forEach((t) => {
    e += un(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / l.length).toFixed(2) + "%"), e / l.length;
}
function gu(l, e, t) {
  var n = this && this.__awaiter || function(g, y, E, k) {
    function w(p) {
      return p instanceof E ? p : new E(function(R) {
        R(p);
      });
    }
    return new (E || (E = Promise))(function(p, R) {
      function b(D) {
        try {
          I(k.next(D));
        } catch (z) {
          R(z);
        }
      }
      function F(D) {
        try {
          I(k.throw(D));
        } catch (z) {
          R(z);
        }
      }
      function I(D) {
        D.done ? p(D.value) : w(D.value).then(b, F);
      }
      I((k = k.apply(g, y || [])).next());
    });
  };
  let { upload_id: i } = e, { root: o } = e, { files: s } = e, { stream_handler: f } = e, r, a = !1, u, c, _ = s.map((g) => Object.assign(Object.assign({}, g), { progress: 0 }));
  const d = _u();
  function m(g, y) {
    t(0, _ = _.map((E) => (E.orig_name === g && (E.progress += y), E)));
  }
  return cu(() => n(void 0, void 0, void 0, function* () {
    if (r = yield f(new URL(`${o}/upload_progress?upload_id=${i}`)), r == null)
      throw new Error("Event source is not defined");
    r.onmessage = function(g) {
      return n(this, void 0, void 0, function* () {
        const y = JSON.parse(g.data);
        a || t(1, a = !0), y.msg === "done" ? (r == null || r.close(), d("done")) : (t(7, u = y), m(y.orig_name, y.chunk_size));
      });
    };
  })), du(() => {
    (r != null || r != null) && r.close();
  }), l.$$set = (g) => {
    "upload_id" in g && t(3, i = g.upload_id), "root" in g && t(4, o = g.root), "files" in g && t(5, s = g.files), "stream_handler" in g && t(6, f = g.stream_handler);
  }, l.$$.update = () => {
    l.$$.dirty & /*files_with_progress*/
    1 && hu(_), l.$$.dirty & /*current_file_upload, files_with_progress*/
    129 && t(2, c = u || _[0]);
  }, [
    _,
    a,
    c,
    i,
    o,
    s,
    f,
    u
  ];
}
class pu extends su {
  constructor(e) {
    super(), fu(this, e, gu, mu, uu, {
      upload_id: 3,
      root: 4,
      files: 5,
      stream_handler: 6
    });
  }
}
const {
  SvelteComponent: bu,
  append: ji,
  attr: ge,
  binding_callbacks: wu,
  bubble: At,
  check_outros: wa,
  create_component: vu,
  create_slot: va,
  destroy_component: ku,
  detach: tl,
  element: Wl,
  empty: ka,
  get_all_dirty_from_scope: ya,
  get_slot_changes: Ea,
  group_outros: Ta,
  init: yu,
  insert: nl,
  listen: Le,
  mount_component: Eu,
  prevent_default: St,
  run_all: Tu,
  safe_not_equal: Au,
  set_style: Aa,
  space: Su,
  stop_propagation: Ct,
  toggle_class: fe,
  transition_in: Et,
  transition_out: zt,
  update_slot_base: Sa
} = window.__gradio__svelte__internal, { createEventDispatcher: Cu, tick: Lu } = window.__gradio__svelte__internal;
function Ru(l) {
  let e, t, n, i, o, s, f, r, a, u, c;
  const _ = (
    /*#slots*/
    l[26].default
  ), d = va(
    _,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = Wl("button"), d && d.c(), t = Su(), n = Wl("input"), ge(n, "aria-label", "file upload"), ge(n, "data-testid", "file-upload"), ge(n, "type", "file"), ge(n, "accept", i = /*accept_file_types*/
      l[16] || void 0), n.multiple = o = /*file_count*/
      l[6] === "multiple" || void 0, ge(n, "webkitdirectory", s = /*file_count*/
      l[6] === "directory" || void 0), ge(n, "mozdirectory", f = /*file_count*/
      l[6] === "directory" || void 0), ge(n, "class", "svelte-1s26xmt"), ge(e, "tabindex", r = /*hidden*/
      l[9] ? -1 : 0), ge(e, "class", "svelte-1s26xmt"), fe(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), fe(
        e,
        "center",
        /*center*/
        l[4]
      ), fe(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), fe(
        e,
        "flex",
        /*flex*/
        l[5]
      ), fe(
        e,
        "disable_click",
        /*disable_click*/
        l[7]
      ), Aa(e, "height", "100%");
    },
    m(m, g) {
      nl(m, e, g), d && d.m(e, null), ji(e, t), ji(e, n), l[34](n), a = !0, u || (c = [
        Le(
          n,
          "change",
          /*load_files_from_upload*/
          l[18]
        ),
        Le(e, "drag", Ct(St(
          /*drag_handler*/
          l[27]
        ))),
        Le(e, "dragstart", Ct(St(
          /*dragstart_handler*/
          l[28]
        ))),
        Le(e, "dragend", Ct(St(
          /*dragend_handler*/
          l[29]
        ))),
        Le(e, "dragover", Ct(St(
          /*dragover_handler*/
          l[30]
        ))),
        Le(e, "dragenter", Ct(St(
          /*dragenter_handler*/
          l[31]
        ))),
        Le(e, "dragleave", Ct(St(
          /*dragleave_handler*/
          l[32]
        ))),
        Le(e, "drop", Ct(St(
          /*drop_handler*/
          l[33]
        ))),
        Le(
          e,
          "click",
          /*open_file_upload*/
          l[13]
        ),
        Le(
          e,
          "drop",
          /*loadFilesFromDrop*/
          l[19]
        ),
        Le(
          e,
          "dragenter",
          /*updateDragging*/
          l[17]
        ),
        Le(
          e,
          "dragleave",
          /*updateDragging*/
          l[17]
        )
      ], u = !0);
    },
    p(m, g) {
      d && d.p && (!a || g[0] & /*$$scope*/
      33554432) && Sa(
        d,
        _,
        m,
        /*$$scope*/
        m[25],
        a ? Ea(
          _,
          /*$$scope*/
          m[25],
          g,
          null
        ) : ya(
          /*$$scope*/
          m[25]
        ),
        null
      ), (!a || g[0] & /*accept_file_types*/
      65536 && i !== (i = /*accept_file_types*/
      m[16] || void 0)) && ge(n, "accept", i), (!a || g[0] & /*file_count*/
      64 && o !== (o = /*file_count*/
      m[6] === "multiple" || void 0)) && (n.multiple = o), (!a || g[0] & /*file_count*/
      64 && s !== (s = /*file_count*/
      m[6] === "directory" || void 0)) && ge(n, "webkitdirectory", s), (!a || g[0] & /*file_count*/
      64 && f !== (f = /*file_count*/
      m[6] === "directory" || void 0)) && ge(n, "mozdirectory", f), (!a || g[0] & /*hidden*/
      512 && r !== (r = /*hidden*/
      m[9] ? -1 : 0)) && ge(e, "tabindex", r), (!a || g[0] & /*hidden*/
      512) && fe(
        e,
        "hidden",
        /*hidden*/
        m[9]
      ), (!a || g[0] & /*center*/
      16) && fe(
        e,
        "center",
        /*center*/
        m[4]
      ), (!a || g[0] & /*boundedheight*/
      8) && fe(
        e,
        "boundedheight",
        /*boundedheight*/
        m[3]
      ), (!a || g[0] & /*flex*/
      32) && fe(
        e,
        "flex",
        /*flex*/
        m[5]
      ), (!a || g[0] & /*disable_click*/
      128) && fe(
        e,
        "disable_click",
        /*disable_click*/
        m[7]
      );
    },
    i(m) {
      a || (Et(d, m), a = !0);
    },
    o(m) {
      zt(d, m), a = !1;
    },
    d(m) {
      m && tl(e), d && d.d(m), l[34](null), u = !1, Tu(c);
    }
  };
}
function Du(l) {
  let e, t, n = !/*hidden*/
  l[9] && Wi(l);
  return {
    c() {
      n && n.c(), e = ka();
    },
    m(i, o) {
      n && n.m(i, o), nl(i, e, o), t = !0;
    },
    p(i, o) {
      /*hidden*/
      i[9] ? n && (Ta(), zt(n, 1, 1, () => {
        n = null;
      }), wa()) : n ? (n.p(i, o), o[0] & /*hidden*/
      512 && Et(n, 1)) : (n = Wi(i), n.c(), Et(n, 1), n.m(e.parentNode, e));
    },
    i(i) {
      t || (Et(n), t = !0);
    },
    o(i) {
      zt(n), t = !1;
    },
    d(i) {
      i && tl(e), n && n.d(i);
    }
  };
}
function Ou(l) {
  let e, t, n, i, o;
  const s = (
    /*#slots*/
    l[26].default
  ), f = va(
    s,
    l,
    /*$$scope*/
    l[25],
    null
  );
  return {
    c() {
      e = Wl("button"), f && f.c(), ge(e, "tabindex", t = /*hidden*/
      l[9] ? -1 : 0), ge(e, "class", "svelte-1s26xmt"), fe(
        e,
        "hidden",
        /*hidden*/
        l[9]
      ), fe(
        e,
        "center",
        /*center*/
        l[4]
      ), fe(
        e,
        "boundedheight",
        /*boundedheight*/
        l[3]
      ), fe(
        e,
        "flex",
        /*flex*/
        l[5]
      ), Aa(e, "height", "100%");
    },
    m(r, a) {
      nl(r, e, a), f && f.m(e, null), n = !0, i || (o = Le(
        e,
        "click",
        /*paste_clipboard*/
        l[12]
      ), i = !0);
    },
    p(r, a) {
      f && f.p && (!n || a[0] & /*$$scope*/
      33554432) && Sa(
        f,
        s,
        r,
        /*$$scope*/
        r[25],
        n ? Ea(
          s,
          /*$$scope*/
          r[25],
          a,
          null
        ) : ya(
          /*$$scope*/
          r[25]
        ),
        null
      ), (!n || a[0] & /*hidden*/
      512 && t !== (t = /*hidden*/
      r[9] ? -1 : 0)) && ge(e, "tabindex", t), (!n || a[0] & /*hidden*/
      512) && fe(
        e,
        "hidden",
        /*hidden*/
        r[9]
      ), (!n || a[0] & /*center*/
      16) && fe(
        e,
        "center",
        /*center*/
        r[4]
      ), (!n || a[0] & /*boundedheight*/
      8) && fe(
        e,
        "boundedheight",
        /*boundedheight*/
        r[3]
      ), (!n || a[0] & /*flex*/
      32) && fe(
        e,
        "flex",
        /*flex*/
        r[5]
      );
    },
    i(r) {
      n || (Et(f, r), n = !0);
    },
    o(r) {
      zt(f, r), n = !1;
    },
    d(r) {
      r && tl(e), f && f.d(r), i = !1, o();
    }
  };
}
function Wi(l) {
  let e, t;
  return e = new pu({
    props: {
      root: (
        /*root*/
        l[8]
      ),
      upload_id: (
        /*upload_id*/
        l[14]
      ),
      files: (
        /*file_data*/
        l[15]
      ),
      stream_handler: (
        /*stream_handler*/
        l[11]
      )
    }
  }), {
    c() {
      vu(e.$$.fragment);
    },
    m(n, i) {
      Eu(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      256 && (o.root = /*root*/
      n[8]), i[0] & /*upload_id*/
      16384 && (o.upload_id = /*upload_id*/
      n[14]), i[0] & /*file_data*/
      32768 && (o.files = /*file_data*/
      n[15]), i[0] & /*stream_handler*/
      2048 && (o.stream_handler = /*stream_handler*/
      n[11]), e.$set(o);
    },
    i(n) {
      t || (Et(e.$$.fragment, n), t = !0);
    },
    o(n) {
      zt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ku(e, n);
    }
  };
}
function Iu(l) {
  let e, t, n, i;
  const o = [Ou, Du, Ru], s = [];
  function f(r, a) {
    return (
      /*filetype*/
      r[0] === "clipboard" ? 0 : (
        /*uploading*/
        r[1] && /*show_progress*/
        r[10] ? 1 : 2
      )
    );
  }
  return e = f(l), t = s[e] = o[e](l), {
    c() {
      t.c(), n = ka();
    },
    m(r, a) {
      s[e].m(r, a), nl(r, n, a), i = !0;
    },
    p(r, a) {
      let u = e;
      e = f(r), e === u ? s[e].p(r, a) : (Ta(), zt(s[u], 1, 1, () => {
        s[u] = null;
      }), wa(), t = s[e], t ? t.p(r, a) : (t = s[e] = o[e](r), t.c()), Et(t, 1), t.m(n.parentNode, n));
    },
    i(r) {
      i || (Et(t), i = !0);
    },
    o(r) {
      zt(t), i = !1;
    },
    d(r) {
      r && tl(n), s[e].d(r);
    }
  };
}
function Mu(l, e, t) {
  if (!l || l === "*" || l === "file/*" || Array.isArray(l) && l.some((i) => i === "*" || i === "file/*"))
    return !0;
  let n;
  if (typeof l == "string")
    n = l.split(",").map((i) => i.trim());
  else if (Array.isArray(l))
    n = l;
  else
    return !1;
  return n.includes(e) || n.some((i) => {
    const [o] = i.split("/").map((s) => s.trim());
    return i.endsWith("/*") && t.startsWith(o + "/");
  });
}
function Nu(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(A, B, K, $) {
    function ae(de) {
      return de instanceof K ? de : new K(function(S) {
        S(de);
      });
    }
    return new (K || (K = Promise))(function(de, S) {
      function W(Q) {
        try {
          ee($.next(Q));
        } catch (ne) {
          S(ne);
        }
      }
      function G(Q) {
        try {
          ee($.throw(Q));
        } catch (ne) {
          S(ne);
        }
      }
      function ee(Q) {
        Q.done ? de(Q.value) : ae(Q.value).then(W, G);
      }
      ee(($ = $.apply(A, B || [])).next());
    });
  };
  let { filetype: s = null } = e, { dragging: f = !1 } = e, { boundedheight: r = !0 } = e, { center: a = !0 } = e, { flex: u = !0 } = e, { file_count: c = "single" } = e, { disable_click: _ = !1 } = e, { root: d } = e, { hidden: m = !1 } = e, { format: g = "file" } = e, { uploading: y = !1 } = e, { hidden_upload: E = null } = e, { show_progress: k = !0 } = e, { max_file_size: w = null } = e, { upload: p } = e, { stream_handler: R } = e, b, F, I;
  const D = Cu(), z = ["image", "video", "audio", "text", "file"], C = (A) => A.startsWith(".") || A.endsWith("/*") ? A : z.includes(A) ? A + "/*" : "." + A;
  function U() {
    t(20, f = !f);
  }
  function ie() {
    navigator.clipboard.read().then((A) => o(this, void 0, void 0, function* () {
      for (let B = 0; B < A.length; B++) {
        const K = A[B].types.find(($) => $.startsWith("image/"));
        if (K) {
          A[B].getType(K).then(($) => o(this, void 0, void 0, function* () {
            const ae = new File([$], `clipboard.${K.replace("image/", "")}`);
            yield Z([ae]);
          }));
          break;
        }
      }
    }));
  }
  function J() {
    _ || E && (t(2, E.value = "", E), E.click());
  }
  function ce(A) {
    return o(this, void 0, void 0, function* () {
      yield Lu(), t(14, b = Math.random().toString(36).substring(2, 15)), t(1, y = !0);
      try {
        const B = yield p(A, d, b, w ?? 1 / 0);
        return D("load", c === "single" ? B == null ? void 0 : B[0] : B), t(1, y = !1), B || [];
      } catch (B) {
        return D("error", B.message), t(1, y = !1), [];
      }
    });
  }
  function Z(A) {
    return o(this, void 0, void 0, function* () {
      if (!A.length)
        return;
      let B = A.map((K) => new File([K], K instanceof File ? K.name : "file", { type: K.type }));
      return t(15, F = yield au(B)), yield ce(F);
    });
  }
  function te(A) {
    return o(this, void 0, void 0, function* () {
      const B = A.target;
      if (B.files)
        if (g != "blob")
          yield Z(Array.from(B.files));
        else {
          if (c === "single") {
            D("load", B.files[0]);
            return;
          }
          D("load", B.files);
        }
    });
  }
  function oe(A) {
    return o(this, void 0, void 0, function* () {
      var B;
      if (t(20, f = !1), !(!((B = A.dataTransfer) === null || B === void 0) && B.files)) return;
      const K = Array.from(A.dataTransfer.files).filter(($) => {
        const ae = "." + $.name.split(".").pop();
        return ae && Mu(I, ae, $.type) || (ae && Array.isArray(s) ? s.includes(ae) : ae === s) ? !0 : (D("error", `Invalid file type only ${s} allowed.`), !1);
      });
      if (g != "blob")
        yield Z(K);
      else {
        if (c === "single") {
          D("load", K[0]);
          return;
        }
        D("load", K);
      }
    });
  }
  function Me(A) {
    At.call(this, l, A);
  }
  function _e(A) {
    At.call(this, l, A);
  }
  function v(A) {
    At.call(this, l, A);
  }
  function ke(A) {
    At.call(this, l, A);
  }
  function V(A) {
    At.call(this, l, A);
  }
  function gt(A) {
    At.call(this, l, A);
  }
  function L(A) {
    At.call(this, l, A);
  }
  function We(A) {
    wu[A ? "unshift" : "push"](() => {
      E = A, t(2, E);
    });
  }
  return l.$$set = (A) => {
    "filetype" in A && t(0, s = A.filetype), "dragging" in A && t(20, f = A.dragging), "boundedheight" in A && t(3, r = A.boundedheight), "center" in A && t(4, a = A.center), "flex" in A && t(5, u = A.flex), "file_count" in A && t(6, c = A.file_count), "disable_click" in A && t(7, _ = A.disable_click), "root" in A && t(8, d = A.root), "hidden" in A && t(9, m = A.hidden), "format" in A && t(21, g = A.format), "uploading" in A && t(1, y = A.uploading), "hidden_upload" in A && t(2, E = A.hidden_upload), "show_progress" in A && t(10, k = A.show_progress), "max_file_size" in A && t(22, w = A.max_file_size), "upload" in A && t(23, p = A.upload), "stream_handler" in A && t(11, R = A.stream_handler), "$$scope" in A && t(25, i = A.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*filetype*/
    1 && (s == null ? t(16, I = null) : typeof s == "string" ? t(16, I = C(s)) : (t(0, s = s.map(C)), t(16, I = s.join(", "))));
  }, [
    s,
    y,
    E,
    r,
    a,
    u,
    c,
    _,
    d,
    m,
    k,
    R,
    ie,
    J,
    b,
    F,
    I,
    U,
    te,
    oe,
    f,
    g,
    w,
    p,
    Z,
    i,
    n,
    Me,
    _e,
    v,
    ke,
    V,
    gt,
    L,
    We
  ];
}
class Pu extends bu {
  constructor(e) {
    super(), yu(
      this,
      e,
      Nu,
      Iu,
      Au,
      {
        filetype: 0,
        dragging: 20,
        boundedheight: 3,
        center: 4,
        flex: 5,
        file_count: 6,
        disable_click: 7,
        root: 8,
        hidden: 9,
        format: 21,
        uploading: 1,
        hidden_upload: 2,
        show_progress: 10,
        max_file_size: 22,
        upload: 23,
        stream_handler: 11,
        paste_clipboard: 12,
        open_file_upload: 13,
        load_files: 24
      },
      null,
      [-1, -1]
    );
  }
  get paste_clipboard() {
    return this.$$.ctx[12];
  }
  get open_file_upload() {
    return this.$$.ctx[13];
  }
  get load_files() {
    return this.$$.ctx[24];
  }
}
const { setContext: Vd, getContext: Fu } = window.__gradio__svelte__internal, zu = "WORKER_PROXY_CONTEXT_KEY";
function Ca() {
  return Fu(zu);
}
function Uu(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function La(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function Ra(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!Uu(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
let Dn;
async function qu(l) {
  if (l == null || !Ra(l))
    return l;
  if (Dn == null)
    try {
      Dn = Ca();
    } catch {
      return l;
    }
  if (Dn == null)
    return l;
  const t = new URL(l, window.location.href).pathname;
  return Dn.httpRequest({
    method: "GET",
    path: t,
    headers: {},
    query_string: ""
  }).then((n) => {
    if (n.status !== 200)
      throw new Error(`Failed to get file ${t} from the Wasm worker.`);
    const i = new Blob([n.body], {
      type: La(n.headers, "content-type")
    });
    return URL.createObjectURL(i);
  });
}
const {
  SvelteComponent: Bu,
  assign: Vn,
  check_outros: Da,
  compute_rest_props: Gi,
  create_slot: ti,
  detach: ll,
  element: Oa,
  empty: Ia,
  exclude_internal_props: Hu,
  get_all_dirty_from_scope: ni,
  get_slot_changes: li,
  get_spread_update: Ma,
  group_outros: Na,
  init: ju,
  insert: il,
  listen: Pa,
  prevent_default: Wu,
  safe_not_equal: Gu,
  set_attributes: Yn,
  transition_in: Ut,
  transition_out: qt,
  update_slot_base: ii
} = window.__gradio__svelte__internal, { createEventDispatcher: Vu } = window.__gradio__svelte__internal;
function Yu(l) {
  let e, t, n, i, o;
  const s = (
    /*#slots*/
    l[8].default
  ), f = ti(
    s,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let r = [
    { href: (
      /*href*/
      l[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      l[1]
    ) },
    /*$$restProps*/
    l[6]
  ], a = {};
  for (let u = 0; u < r.length; u += 1)
    a = Vn(a, r[u]);
  return {
    c() {
      e = Oa("a"), f && f.c(), Yn(e, a);
    },
    m(u, c) {
      il(u, e, c), f && f.m(e, null), n = !0, i || (o = Pa(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(u, c) {
      f && f.p && (!n || c & /*$$scope*/
      128) && ii(
        f,
        s,
        u,
        /*$$scope*/
        u[7],
        n ? li(
          s,
          /*$$scope*/
          u[7],
          c,
          null
        ) : ni(
          /*$$scope*/
          u[7]
        ),
        null
      ), Yn(e, a = Ma(r, [
        (!n || c & /*href*/
        1) && { href: (
          /*href*/
          u[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!n || c & /*download*/
        2) && { download: (
          /*download*/
          u[1]
        ) },
        c & /*$$restProps*/
        64 && /*$$restProps*/
        u[6]
      ]));
    },
    i(u) {
      n || (Ut(f, u), n = !0);
    },
    o(u) {
      qt(f, u), n = !1;
    },
    d(u) {
      u && ll(e), f && f.d(u), i = !1, o();
    }
  };
}
function Xu(l) {
  let e, t, n, i;
  const o = [Ku, Zu], s = [];
  function f(r, a) {
    return (
      /*is_downloading*/
      r[2] ? 0 : 1
    );
  }
  return e = f(l), t = s[e] = o[e](l), {
    c() {
      t.c(), n = Ia();
    },
    m(r, a) {
      s[e].m(r, a), il(r, n, a), i = !0;
    },
    p(r, a) {
      let u = e;
      e = f(r), e === u ? s[e].p(r, a) : (Na(), qt(s[u], 1, 1, () => {
        s[u] = null;
      }), Da(), t = s[e], t ? t.p(r, a) : (t = s[e] = o[e](r), t.c()), Ut(t, 1), t.m(n.parentNode, n));
    },
    i(r) {
      i || (Ut(t), i = !0);
    },
    o(r) {
      qt(t), i = !1;
    },
    d(r) {
      r && ll(n), s[e].d(r);
    }
  };
}
function Zu(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[8].default
  ), s = ti(
    o,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let f = [
    /*$$restProps*/
    l[6],
    { href: (
      /*href*/
      l[0]
    ) }
  ], r = {};
  for (let a = 0; a < f.length; a += 1)
    r = Vn(r, f[a]);
  return {
    c() {
      e = Oa("a"), s && s.c(), Yn(e, r);
    },
    m(a, u) {
      il(a, e, u), s && s.m(e, null), t = !0, n || (i = Pa(e, "click", Wu(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(a, u) {
      s && s.p && (!t || u & /*$$scope*/
      128) && ii(
        s,
        o,
        a,
        /*$$scope*/
        a[7],
        t ? li(
          o,
          /*$$scope*/
          a[7],
          u,
          null
        ) : ni(
          /*$$scope*/
          a[7]
        ),
        null
      ), Yn(e, r = Ma(f, [
        u & /*$$restProps*/
        64 && /*$$restProps*/
        a[6],
        (!t || u & /*href*/
        1) && { href: (
          /*href*/
          a[0]
        ) }
      ]));
    },
    i(a) {
      t || (Ut(s, a), t = !0);
    },
    o(a) {
      qt(s, a), t = !1;
    },
    d(a) {
      a && ll(e), s && s.d(a), n = !1, i();
    }
  };
}
function Ku(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = ti(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      128) && ii(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? li(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : ni(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (Ut(n, i), e = !0);
    },
    o(i) {
      qt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ju(l) {
  let e, t, n, i, o;
  const s = [Xu, Yu], f = [];
  function r(a, u) {
    return u & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (a[4] && Ra(
      /*href*/
      a[0]
    ))), e ? 0 : 1;
  }
  return t = r(l, -1), n = f[t] = s[t](l), {
    c() {
      n.c(), i = Ia();
    },
    m(a, u) {
      f[t].m(a, u), il(a, i, u), o = !0;
    },
    p(a, [u]) {
      let c = t;
      t = r(a, u), t === c ? f[t].p(a, u) : (Na(), qt(f[c], 1, 1, () => {
        f[c] = null;
      }), Da(), n = f[t], n ? n.p(a, u) : (n = f[t] = s[t](a), n.c()), Ut(n, 1), n.m(i.parentNode, i));
    },
    i(a) {
      o || (Ut(n), o = !0);
    },
    o(a) {
      qt(n), o = !1;
    },
    d(a) {
      a && ll(i), f[t].d(a);
    }
  };
}
function Qu(l, e, t) {
  const n = ["href", "download"];
  let i = Gi(e, n), { $$slots: o = {}, $$scope: s } = e;
  var f = this && this.__awaiter || function(m, g, y, E) {
    function k(w) {
      return w instanceof y ? w : new y(function(p) {
        p(w);
      });
    }
    return new (y || (y = Promise))(function(w, p) {
      function R(I) {
        try {
          F(E.next(I));
        } catch (D) {
          p(D);
        }
      }
      function b(I) {
        try {
          F(E.throw(I));
        } catch (D) {
          p(D);
        }
      }
      function F(I) {
        I.done ? w(I.value) : k(I.value).then(R, b);
      }
      F((E = E.apply(m, g || [])).next());
    });
  };
  let { href: r = void 0 } = e, { download: a } = e;
  const u = Vu();
  let c = !1;
  const _ = Ca();
  function d() {
    return f(this, void 0, void 0, function* () {
      if (c)
        return;
      if (u("click"), r == null)
        throw new Error("href is not defined.");
      if (_ == null)
        throw new Error("Wasm worker proxy is not available.");
      const g = new URL(r, window.location.href).pathname;
      t(2, c = !0), _.httpRequest({
        method: "GET",
        path: g,
        headers: {},
        query_string: ""
      }).then((y) => {
        if (y.status !== 200)
          throw new Error(`Failed to get file ${g} from the Wasm worker.`);
        const E = new Blob(
          [y.body],
          {
            type: La(y.headers, "content-type")
          }
        ), k = URL.createObjectURL(E), w = document.createElement("a");
        w.href = k, w.download = a, w.click(), URL.revokeObjectURL(k);
      }).finally(() => {
        t(2, c = !1);
      });
    });
  }
  return l.$$set = (m) => {
    e = Vn(Vn({}, e), Hu(m)), t(6, i = Gi(e, n)), "href" in m && t(0, r = m.href), "download" in m && t(1, a = m.download), "$$scope" in m && t(7, s = m.$$scope);
  }, [
    r,
    a,
    c,
    u,
    _,
    d,
    i,
    s,
    o
  ];
}
class Fa extends Bu {
  constructor(e) {
    super(), ju(this, e, Qu, Ju, Gu, { href: 0, download: 1 });
  }
}
const {
  SvelteComponent: xu,
  append: Sl,
  attr: $u,
  check_outros: Cl,
  create_component: dn,
  destroy_component: mn,
  detach: ec,
  element: tc,
  group_outros: Ll,
  init: nc,
  insert: lc,
  mount_component: hn,
  safe_not_equal: ic,
  set_style: Vi,
  space: Rl,
  toggle_class: Yi,
  transition_in: Te,
  transition_out: Je
} = window.__gradio__svelte__internal, { createEventDispatcher: oc } = window.__gradio__svelte__internal;
function Xi(l) {
  let e, t;
  return e = new Bt({
    props: {
      Icon: Ks,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      dn(e.$$.fragment);
    },
    m(n, i) {
      hn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.edit")), e.$set(o);
    },
    i(n) {
      t || (Te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      mn(e, n);
    }
  };
}
function Zi(l) {
  let e, t;
  return e = new Bt({
    props: {
      Icon: Tf,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      dn(e.$$.fragment);
    },
    m(n, i) {
      hn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.undo")), e.$set(o);
    },
    i(n) {
      t || (Te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      mn(e, n);
    }
  };
}
function Ki(l) {
  let e, t;
  return e = new Fa({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: { default: [ac] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      dn(e.$$.fragment);
    },
    m(n, i) {
      hn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      mn(e, n);
    }
  };
}
function ac(l) {
  let e, t;
  return e = new Bt({
    props: {
      Icon: ca,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      dn(e.$$.fragment);
    },
    m(n, i) {
      hn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.download")), e.$set(o);
    },
    i(n) {
      t || (Te(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      mn(e, n);
    }
  };
}
function rc(l) {
  let e, t, n, i, o, s, f = (
    /*editable*/
    l[0] && Xi(l)
  ), r = (
    /*undoable*/
    l[1] && Zi(l)
  ), a = (
    /*download*/
    l[2] && Ki(l)
  );
  return o = new Bt({
    props: {
      Icon: ua,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = tc("div"), f && f.c(), t = Rl(), r && r.c(), n = Rl(), a && a.c(), i = Rl(), dn(o.$$.fragment), $u(e, "class", "svelte-1wj0ocy"), Yi(e, "not-absolute", !/*absolute*/
      l[3]), Vi(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(u, c) {
      lc(u, e, c), f && f.m(e, null), Sl(e, t), r && r.m(e, null), Sl(e, n), a && a.m(e, null), Sl(e, i), hn(o, e, null), s = !0;
    },
    p(u, [c]) {
      /*editable*/
      u[0] ? f ? (f.p(u, c), c & /*editable*/
      1 && Te(f, 1)) : (f = Xi(u), f.c(), Te(f, 1), f.m(e, t)) : f && (Ll(), Je(f, 1, 1, () => {
        f = null;
      }), Cl()), /*undoable*/
      u[1] ? r ? (r.p(u, c), c & /*undoable*/
      2 && Te(r, 1)) : (r = Zi(u), r.c(), Te(r, 1), r.m(e, n)) : r && (Ll(), Je(r, 1, 1, () => {
        r = null;
      }), Cl()), /*download*/
      u[2] ? a ? (a.p(u, c), c & /*download*/
      4 && Te(a, 1)) : (a = Ki(u), a.c(), Te(a, 1), a.m(e, i)) : a && (Ll(), Je(a, 1, 1, () => {
        a = null;
      }), Cl());
      const _ = {};
      c & /*i18n*/
      16 && (_.label = /*i18n*/
      u[4]("common.clear")), o.$set(_), (!s || c & /*absolute*/
      8) && Yi(e, "not-absolute", !/*absolute*/
      u[3]), c & /*absolute*/
      8 && Vi(
        e,
        "position",
        /*absolute*/
        u[3] ? "absolute" : "static"
      );
    },
    i(u) {
      s || (Te(f), Te(r), Te(a), Te(o.$$.fragment, u), s = !0);
    },
    o(u) {
      Je(f), Je(r), Je(a), Je(o.$$.fragment, u), s = !1;
    },
    d(u) {
      u && ec(e), f && f.d(), r && r.d(), a && a.d(), mn(o);
    }
  };
}
function sc(l, e, t) {
  let { editable: n = !1 } = e, { undoable: i = !1 } = e, { download: o = null } = e, { absolute: s = !0 } = e, { i18n: f } = e;
  const r = oc(), a = () => r("edit"), u = () => r("undo"), c = (_) => {
    r("clear"), _.stopPropagation();
  };
  return l.$$set = (_) => {
    "editable" in _ && t(0, n = _.editable), "undoable" in _ && t(1, i = _.undoable), "download" in _ && t(2, o = _.download), "absolute" in _ && t(3, s = _.absolute), "i18n" in _ && t(4, f = _.i18n);
  }, [
    n,
    i,
    o,
    s,
    f,
    r,
    a,
    u,
    c
  ];
}
class oi extends xu {
  constructor(e) {
    super(), nc(this, e, sc, rc, ic, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
const {
  SvelteComponent: fc,
  assign: Gl,
  compute_rest_props: Ji,
  detach: uc,
  element: cc,
  exclude_internal_props: _c,
  get_spread_update: dc,
  init: mc,
  insert: hc,
  listen: gc,
  noop: Qi,
  safe_not_equal: pc,
  set_attributes: xi,
  src_url_equal: bc,
  toggle_class: $i
} = window.__gradio__svelte__internal, { createEventDispatcher: wc } = window.__gradio__svelte__internal;
function vc(l) {
  let e, t, n, i, o = [
    {
      src: t = /*resolved_src*/
      l[0]
    },
    /*$$restProps*/
    l[2]
  ], s = {};
  for (let f = 0; f < o.length; f += 1)
    s = Gl(s, o[f]);
  return {
    c() {
      e = cc("img"), xi(e, s), $i(e, "svelte-kxeri3", !0);
    },
    m(f, r) {
      hc(f, e, r), n || (i = gc(
        e,
        "load",
        /*load_handler*/
        l[5]
      ), n = !0);
    },
    p(f, [r]) {
      xi(e, s = dc(o, [
        r & /*resolved_src*/
        1 && !bc(e.src, t = /*resolved_src*/
        f[0]) && { src: t },
        r & /*$$restProps*/
        4 && /*$$restProps*/
        f[2]
      ])), $i(e, "svelte-kxeri3", !0);
    },
    i: Qi,
    o: Qi,
    d(f) {
      f && uc(e), n = !1, i();
    }
  };
}
function kc(l, e, t) {
  const n = ["src"];
  let i = Ji(e, n);
  const o = wc();
  let { src: s = void 0 } = e, f, r;
  const a = () => o("load");
  return l.$$set = (u) => {
    e = Gl(Gl({}, e), _c(u)), t(2, i = Ji(e, n)), "src" in u && t(3, s = u.src);
  }, l.$$.update = () => {
    if (l.$$.dirty & /*src, latest_src*/
    24) {
      t(0, f = s), t(4, r = s);
      const u = s;
      qu(u).then((c) => {
        r === u && t(0, f = c);
      });
    }
  }, [f, o, i, s, r, a];
}
class ai extends fc {
  constructor(e) {
    super(), mc(this, e, kc, vc, pc, { src: 3 });
  }
}
var eo = Object.prototype.hasOwnProperty;
function to(l, e, t) {
  for (t of l.keys())
    if (cn(t, e)) return t;
}
function cn(l, e) {
  var t, n, i;
  if (l === e) return !0;
  if (l && e && (t = l.constructor) === e.constructor) {
    if (t === Date) return l.getTime() === e.getTime();
    if (t === RegExp) return l.toString() === e.toString();
    if (t === Array) {
      if ((n = l.length) === e.length)
        for (; n-- && cn(l[n], e[n]); ) ;
      return n === -1;
    }
    if (t === Set) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n, i && typeof i == "object" && (i = to(e, i), !i) || !e.has(i)) return !1;
      return !0;
    }
    if (t === Map) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n[0], i && typeof i == "object" && (i = to(e, i), !i) || !cn(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      l = new Uint8Array(l), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l.getInt8(n) === e.getInt8(n); ) ;
      return n === -1;
    }
    if (ArrayBuffer.isView(l)) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l[n] === e[n]; ) ;
      return n === -1;
    }
    if (!t || typeof l == "object") {
      n = 0;
      for (t in l)
        if (eo.call(l, t) && ++n && !eo.call(e, t) || !(t in e) || !cn(l[t], e[t])) return !1;
      return Object.keys(e).length === n;
    }
  }
  return l !== l && e !== e;
}
async function yc(l) {
  return l ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(
    l.map(async ([t, n]) => t === null || !t.url ? "" : await Mf(t.url))
  )).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
const {
  SvelteComponent: Ec,
  add_render_callback: Tc,
  append: we,
  attr: re,
  binding_callbacks: no,
  bubble: lo,
  check_outros: vt,
  create_component: st,
  destroy_component: ft,
  destroy_each: za,
  detach: qe,
  element: Oe,
  empty: Ac,
  ensure_array_like: Xn,
  globals: Sc,
  group_outros: kt,
  init: Cc,
  insert: Be,
  listen: _n,
  mount_component: ut,
  run_all: Lc,
  safe_not_equal: Rc,
  set_data: Ua,
  set_style: it,
  space: xe,
  text: qa,
  toggle_class: ze,
  transition_in: j,
  transition_out: X
} = window.__gradio__svelte__internal, { window: Ba } = Sc, { createEventDispatcher: Dc } = window.__gradio__svelte__internal, { tick: Oc } = window.__gradio__svelte__internal;
function io(l, e, t) {
  const n = l.slice();
  return n[46] = e[t], n[48] = t, n;
}
function oo(l, e, t) {
  const n = l.slice();
  return n[49] = e[t], n[50] = e, n[48] = t, n;
}
function ao(l) {
  let e, t;
  return e = new ra({
    props: {
      show_label: (
        /*show_label*/
        l[1]
      ),
      Icon: _a,
      label: (
        /*label*/
        l[2] || "Gallery"
      )
    }
  }), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      ut(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      2 && (o.show_label = /*show_label*/
      n[1]), i[0] & /*label*/
      4 && (o.label = /*label*/
      n[2] || "Gallery"), e.$set(o);
    },
    i(n) {
      t || (j(e.$$.fragment, n), t = !0);
    },
    o(n) {
      X(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ft(e, n);
    }
  };
}
function Ic(l) {
  let e, t, n, i, o, s, f = (
    /*selected_image*/
    l[18] && /*allow_preview*/
    l[7] && ro(l)
  ), r = (
    /*interactive*/
    l[12] && co(l)
  ), a = (
    /*show_share_button*/
    l[9] && _o(l)
  ), u = Xn(
    /*resolved_value*/
    l[14]
  ), c = [];
  for (let d = 0; d < u.length; d += 1)
    c[d] = ho(io(l, u, d));
  const _ = (d) => X(c[d], 1, 1, () => {
    c[d] = null;
  });
  return {
    c() {
      f && f.c(), e = xe(), t = Oe("div"), n = Oe("div"), r && r.c(), i = xe(), a && a.c(), o = xe();
      for (let d = 0; d < c.length; d += 1)
        c[d].c();
      re(n, "class", "grid-container svelte-94ql7d"), it(
        n,
        "--grid-cols",
        /*columns*/
        l[4]
      ), it(
        n,
        "--grid-rows",
        /*rows*/
        l[5]
      ), it(
        n,
        "--object-fit",
        /*object_fit*/
        l[8]
      ), it(
        n,
        "height",
        /*height*/
        l[6]
      ), ze(
        n,
        "pt-6",
        /*show_label*/
        l[1]
      ), re(t, "class", "grid-wrap svelte-94ql7d"), ze(
        t,
        "minimal",
        /*mode*/
        l[13] === "minimal"
      ), ze(
        t,
        "fixed-height",
        /*mode*/
        l[13] !== "minimal" && (!/*height*/
        l[6] || /*height*/
        l[6] == "auto")
      );
    },
    m(d, m) {
      f && f.m(d, m), Be(d, e, m), Be(d, t, m), we(t, n), r && r.m(n, null), we(n, i), a && a.m(n, null), we(n, o);
      for (let g = 0; g < c.length; g += 1)
        c[g] && c[g].m(n, null);
      s = !0;
    },
    p(d, m) {
      if (/*selected_image*/
      d[18] && /*allow_preview*/
      d[7] ? f ? (f.p(d, m), m[0] & /*selected_image, allow_preview*/
      262272 && j(f, 1)) : (f = ro(d), f.c(), j(f, 1), f.m(e.parentNode, e)) : f && (kt(), X(f, 1, 1, () => {
        f = null;
      }), vt()), /*interactive*/
      d[12] ? r ? (r.p(d, m), m[0] & /*interactive*/
      4096 && j(r, 1)) : (r = co(d), r.c(), j(r, 1), r.m(n, i)) : r && (kt(), X(r, 1, 1, () => {
        r = null;
      }), vt()), /*show_share_button*/
      d[9] ? a ? (a.p(d, m), m[0] & /*show_share_button*/
      512 && j(a, 1)) : (a = _o(d), a.c(), j(a, 1), a.m(n, o)) : a && (kt(), X(a, 1, 1, () => {
        a = null;
      }), vt()), m[0] & /*resolved_value, selected_index*/
      16385) {
        u = Xn(
          /*resolved_value*/
          d[14]
        );
        let g;
        for (g = 0; g < u.length; g += 1) {
          const y = io(d, u, g);
          c[g] ? (c[g].p(y, m), j(c[g], 1)) : (c[g] = ho(y), c[g].c(), j(c[g], 1), c[g].m(n, null));
        }
        for (kt(), g = u.length; g < c.length; g += 1)
          _(g);
        vt();
      }
      (!s || m[0] & /*columns*/
      16) && it(
        n,
        "--grid-cols",
        /*columns*/
        d[4]
      ), (!s || m[0] & /*rows*/
      32) && it(
        n,
        "--grid-rows",
        /*rows*/
        d[5]
      ), (!s || m[0] & /*object_fit*/
      256) && it(
        n,
        "--object-fit",
        /*object_fit*/
        d[8]
      ), (!s || m[0] & /*height*/
      64) && it(
        n,
        "height",
        /*height*/
        d[6]
      ), (!s || m[0] & /*show_label*/
      2) && ze(
        n,
        "pt-6",
        /*show_label*/
        d[1]
      ), (!s || m[0] & /*mode*/
      8192) && ze(
        t,
        "minimal",
        /*mode*/
        d[13] === "minimal"
      ), (!s || m[0] & /*mode, height*/
      8256) && ze(
        t,
        "fixed-height",
        /*mode*/
        d[13] !== "minimal" && (!/*height*/
        d[6] || /*height*/
        d[6] == "auto")
      );
    },
    i(d) {
      if (!s) {
        j(f), j(r), j(a);
        for (let m = 0; m < u.length; m += 1)
          j(c[m]);
        s = !0;
      }
    },
    o(d) {
      X(f), X(r), X(a), c = c.filter(Boolean);
      for (let m = 0; m < c.length; m += 1)
        X(c[m]);
      s = !1;
    },
    d(d) {
      d && (qe(e), qe(t)), f && f.d(d), r && r.d(), a && a.d(), za(c, d);
    }
  };
}
function Mc(l) {
  let e, t;
  return e = new vs({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Nc] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      ut(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      1048576 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (j(e.$$.fragment, n), t = !0);
    },
    o(n) {
      X(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ft(e, n);
    }
  };
}
function ro(l) {
  var w;
  let e, t, n, i, o, s, f, r, a, u, c, _, d, m = (
    /*show_download_button*/
    l[10] && so(l)
  );
  i = new oi({
    props: { i18n: (
      /*i18n*/
      l[11]
    ), absolute: !1 }
  }), i.$on(
    "clear",
    /*clear_handler*/
    l[33]
  ), f = new ai({
    props: {
      "data-testid": "detailed-image",
      src: (
        /*selected_image*/
        l[18].image.url
      ),
      alt: (
        /*selected_image*/
        l[18].caption || ""
      ),
      title: (
        /*selected_image*/
        l[18].caption || null
      ),
      class: (
        /*selected_image*/
        l[18].caption && "with-caption"
      ),
      loading: "lazy"
    }
  });
  let g = (
    /*selected_image*/
    ((w = l[18]) == null ? void 0 : w.caption) && fo(l)
  ), y = Xn(
    /*resolved_value*/
    l[14]
  ), E = [];
  for (let p = 0; p < y.length; p += 1)
    E[p] = uo(oo(l, y, p));
  const k = (p) => X(E[p], 1, 1, () => {
    E[p] = null;
  });
  return {
    c() {
      e = Oe("button"), t = Oe("div"), m && m.c(), n = xe(), st(i.$$.fragment), o = xe(), s = Oe("button"), st(f.$$.fragment), r = xe(), g && g.c(), a = xe(), u = Oe("div");
      for (let p = 0; p < E.length; p += 1)
        E[p].c();
      re(t, "class", "icon-buttons svelte-94ql7d"), re(s, "class", "image-button svelte-94ql7d"), it(s, "height", "calc(100% - " + /*selected_image*/
      (l[18].caption ? "80px" : "60px") + ")"), re(s, "aria-label", "detailed view of selected image"), re(u, "class", "thumbnails scroll-hide svelte-94ql7d"), re(u, "data-testid", "container_el"), re(e, "class", "preview svelte-94ql7d"), ze(
        e,
        "minimal",
        /*mode*/
        l[13] === "minimal"
      );
    },
    m(p, R) {
      Be(p, e, R), we(e, t), m && m.m(t, null), we(t, n), ut(i, t, null), we(e, o), we(e, s), ut(f, s, null), we(e, r), g && g.m(e, null), we(e, a), we(e, u);
      for (let b = 0; b < E.length; b += 1)
        E[b] && E[b].m(u, null);
      l[37](u), c = !0, _ || (d = [
        _n(
          s,
          "click",
          /*click_handler_1*/
          l[34]
        ),
        _n(
          e,
          "keydown",
          /*on_keydown*/
          l[21]
        )
      ], _ = !0);
    },
    p(p, R) {
      var I;
      /*show_download_button*/
      p[10] ? m ? (m.p(p, R), R[0] & /*show_download_button*/
      1024 && j(m, 1)) : (m = so(p), m.c(), j(m, 1), m.m(t, n)) : m && (kt(), X(m, 1, 1, () => {
        m = null;
      }), vt());
      const b = {};
      R[0] & /*i18n*/
      2048 && (b.i18n = /*i18n*/
      p[11]), i.$set(b);
      const F = {};
      if (R[0] & /*selected_image*/
      262144 && (F.src = /*selected_image*/
      p[18].image.url), R[0] & /*selected_image*/
      262144 && (F.alt = /*selected_image*/
      p[18].caption || ""), R[0] & /*selected_image*/
      262144 && (F.title = /*selected_image*/
      p[18].caption || null), R[0] & /*selected_image*/
      262144 && (F.class = /*selected_image*/
      p[18].caption && "with-caption"), f.$set(F), (!c || R[0] & /*selected_image*/
      262144) && it(s, "height", "calc(100% - " + /*selected_image*/
      (p[18].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (I = p[18]) != null && I.caption ? g ? g.p(p, R) : (g = fo(p), g.c(), g.m(e, a)) : g && (g.d(1), g = null), R[0] & /*resolved_value, el, selected_index, mode*/
      57345) {
        y = Xn(
          /*resolved_value*/
          p[14]
        );
        let D;
        for (D = 0; D < y.length; D += 1) {
          const z = oo(p, y, D);
          E[D] ? (E[D].p(z, R), j(E[D], 1)) : (E[D] = uo(z), E[D].c(), j(E[D], 1), E[D].m(u, null));
        }
        for (kt(), D = y.length; D < E.length; D += 1)
          k(D);
        vt();
      }
      (!c || R[0] & /*mode*/
      8192) && ze(
        e,
        "minimal",
        /*mode*/
        p[13] === "minimal"
      );
    },
    i(p) {
      if (!c) {
        j(m), j(i.$$.fragment, p), j(f.$$.fragment, p);
        for (let R = 0; R < y.length; R += 1)
          j(E[R]);
        c = !0;
      }
    },
    o(p) {
      X(m), X(i.$$.fragment, p), X(f.$$.fragment, p), E = E.filter(Boolean);
      for (let R = 0; R < E.length; R += 1)
        X(E[R]);
      c = !1;
    },
    d(p) {
      p && qe(e), m && m.d(), ft(i), ft(f), g && g.d(), za(E, p), l[37](null), _ = !1, Lc(d);
    }
  };
}
function so(l) {
  let e, t, n;
  return t = new Bt({
    props: {
      Icon: ca,
      label: (
        /*i18n*/
        l[11]("common.download")
      )
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  ), {
    c() {
      e = Oe("div"), st(t.$$.fragment), re(e, "class", "download-button-container svelte-94ql7d");
    },
    m(i, o) {
      Be(i, e, o), ut(t, e, null), n = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      2048 && (s.label = /*i18n*/
      i[11]("common.download")), t.$set(s);
    },
    i(i) {
      n || (j(t.$$.fragment, i), n = !0);
    },
    o(i) {
      X(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && qe(e), ft(t);
    }
  };
}
function fo(l) {
  let e, t = (
    /*selected_image*/
    l[18].caption + ""
  ), n;
  return {
    c() {
      e = Oe("caption"), n = qa(t), re(e, "class", "caption svelte-94ql7d");
    },
    m(i, o) {
      Be(i, e, o), we(e, n);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      262144 && t !== (t = /*selected_image*/
      i[18].caption + "") && Ua(n, t);
    },
    d(i) {
      i && qe(e);
    }
  };
}
function uo(l) {
  let e, t, n, i, o = (
    /*i*/
    l[48]
  ), s, f, r;
  t = new ai({
    props: {
      src: (
        /*image*/
        l[49].image.url
      ),
      title: (
        /*image*/
        l[49].caption || null
      ),
      "data-testid": "thumbnail " + /*i*/
      (l[48] + 1),
      alt: "",
      loading: "lazy"
    }
  });
  const a = () => (
    /*button_binding*/
    l[35](e, o)
  ), u = () => (
    /*button_binding*/
    l[35](null, o)
  );
  function c() {
    return (
      /*click_handler_2*/
      l[36](
        /*i*/
        l[48]
      )
    );
  }
  return {
    c() {
      e = Oe("button"), st(t.$$.fragment), n = xe(), re(e, "class", "thumbnail-item thumbnail-small svelte-94ql7d"), re(e, "aria-label", i = "Thumbnail " + /*i*/
      (l[48] + 1) + " of " + /*resolved_value*/
      l[14].length), ze(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[48] && /*mode*/
        l[13] !== "minimal"
      );
    },
    m(_, d) {
      Be(_, e, d), ut(t, e, null), we(e, n), a(), s = !0, f || (r = _n(e, "click", c), f = !0);
    },
    p(_, d) {
      l = _;
      const m = {};
      d[0] & /*resolved_value*/
      16384 && (m.src = /*image*/
      l[49].image.url), d[0] & /*resolved_value*/
      16384 && (m.title = /*image*/
      l[49].caption || null), t.$set(m), (!s || d[0] & /*resolved_value*/
      16384 && i !== (i = "Thumbnail " + /*i*/
      (l[48] + 1) + " of " + /*resolved_value*/
      l[14].length)) && re(e, "aria-label", i), o !== /*i*/
      l[48] && (u(), o = /*i*/
      l[48], a()), (!s || d[0] & /*selected_index, mode*/
      8193) && ze(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[48] && /*mode*/
        l[13] !== "minimal"
      );
    },
    i(_) {
      s || (j(t.$$.fragment, _), s = !0);
    },
    o(_) {
      X(t.$$.fragment, _), s = !1;
    },
    d(_) {
      _ && qe(e), ft(t), u(), f = !1, r();
    }
  };
}
function co(l) {
  let e, t, n;
  return t = new oi({
    props: { i18n: (
      /*i18n*/
      l[11]
    ), absolute: !1 }
  }), t.$on(
    "clear",
    /*clear_handler_1*/
    l[38]
  ), {
    c() {
      e = Oe("div"), st(t.$$.fragment), re(e, "class", "icon-button svelte-94ql7d");
    },
    m(i, o) {
      Be(i, e, o), ut(t, e, null), n = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      2048 && (s.i18n = /*i18n*/
      i[11]), t.$set(s);
    },
    i(i) {
      n || (j(t.$$.fragment, i), n = !0);
    },
    o(i) {
      X(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && qe(e), ft(t);
    }
  };
}
function _o(l) {
  let e, t, n;
  return t = new Vf({
    props: {
      i18n: (
        /*i18n*/
        l[11]
      ),
      value: (
        /*resolved_value*/
        l[14]
      ),
      formatter: yc
    }
  }), t.$on(
    "share",
    /*share_handler*/
    l[39]
  ), t.$on(
    "error",
    /*error_handler*/
    l[40]
  ), {
    c() {
      e = Oe("div"), st(t.$$.fragment), re(e, "class", "icon-button svelte-94ql7d");
    },
    m(i, o) {
      Be(i, e, o), ut(t, e, null), n = !0;
    },
    p(i, o) {
      const s = {};
      o[0] & /*i18n*/
      2048 && (s.i18n = /*i18n*/
      i[11]), o[0] & /*resolved_value*/
      16384 && (s.value = /*resolved_value*/
      i[14]), t.$set(s);
    },
    i(i) {
      n || (j(t.$$.fragment, i), n = !0);
    },
    o(i) {
      X(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && qe(e), ft(t);
    }
  };
}
function mo(l) {
  let e, t = (
    /*entry*/
    l[46].caption + ""
  ), n;
  return {
    c() {
      e = Oe("div"), n = qa(t), re(e, "class", "caption-label svelte-94ql7d");
    },
    m(i, o) {
      Be(i, e, o), we(e, n);
    },
    p(i, o) {
      o[0] & /*resolved_value*/
      16384 && t !== (t = /*entry*/
      i[46].caption + "") && Ua(n, t);
    },
    d(i) {
      i && qe(e);
    }
  };
}
function ho(l) {
  let e, t, n, i, o, s, f, r;
  t = new ai({
    props: {
      alt: (
        /*entry*/
        l[46].caption || ""
      ),
      src: typeof /*entry*/
      l[46].image == "string" ? (
        /*entry*/
        l[46].image
      ) : (
        /*entry*/
        l[46].image.url
      ),
      loading: "lazy"
    }
  });
  let a = (
    /*entry*/
    l[46].caption && mo(l)
  );
  function u() {
    return (
      /*click_handler_3*/
      l[41](
        /*i*/
        l[48]
      )
    );
  }
  return {
    c() {
      e = Oe("button"), st(t.$$.fragment), n = xe(), a && a.c(), i = xe(), re(e, "class", "thumbnail-item thumbnail-lg svelte-94ql7d"), re(e, "aria-label", o = "Thumbnail " + /*i*/
      (l[48] + 1) + " of " + /*resolved_value*/
      l[14].length), ze(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[48]
      );
    },
    m(c, _) {
      Be(c, e, _), ut(t, e, null), we(e, n), a && a.m(e, null), we(e, i), s = !0, f || (r = _n(e, "click", u), f = !0);
    },
    p(c, _) {
      l = c;
      const d = {};
      _[0] & /*resolved_value*/
      16384 && (d.alt = /*entry*/
      l[46].caption || ""), _[0] & /*resolved_value*/
      16384 && (d.src = typeof /*entry*/
      l[46].image == "string" ? (
        /*entry*/
        l[46].image
      ) : (
        /*entry*/
        l[46].image.url
      )), t.$set(d), /*entry*/
      l[46].caption ? a ? a.p(l, _) : (a = mo(l), a.c(), a.m(e, i)) : a && (a.d(1), a = null), (!s || _[0] & /*resolved_value*/
      16384 && o !== (o = "Thumbnail " + /*i*/
      (l[48] + 1) + " of " + /*resolved_value*/
      l[14].length)) && re(e, "aria-label", o), (!s || _[0] & /*selected_index*/
      1) && ze(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[48]
      );
    },
    i(c) {
      s || (j(t.$$.fragment, c), s = !0);
    },
    o(c) {
      X(t.$$.fragment, c), s = !1;
    },
    d(c) {
      c && qe(e), ft(t), a && a.d(), f = !1, r();
    }
  };
}
function Nc(l) {
  let e, t;
  return e = new _a({}), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      ut(e, n, i), t = !0;
    },
    i(n) {
      t || (j(e.$$.fragment, n), t = !0);
    },
    o(n) {
      X(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ft(e, n);
    }
  };
}
function Pc(l) {
  let e, t, n, i, o, s, f;
  Tc(
    /*onwindowresize*/
    l[31]
  );
  let r = (
    /*show_label*/
    l[1] && ao(l)
  );
  const a = [Mc, Ic], u = [];
  function c(_, d) {
    return (
      /*value*/
      _[3] == null || /*resolved_value*/
      _[14] == null || /*resolved_value*/
      _[14].length === 0 ? 0 : 1
    );
  }
  return t = c(l), n = u[t] = a[t](l), {
    c() {
      r && r.c(), e = xe(), n.c(), i = Ac();
    },
    m(_, d) {
      r && r.m(_, d), Be(_, e, d), u[t].m(_, d), Be(_, i, d), o = !0, s || (f = _n(
        Ba,
        "resize",
        /*onwindowresize*/
        l[31]
      ), s = !0);
    },
    p(_, d) {
      /*show_label*/
      _[1] ? r ? (r.p(_, d), d[0] & /*show_label*/
      2 && j(r, 1)) : (r = ao(_), r.c(), j(r, 1), r.m(e.parentNode, e)) : r && (kt(), X(r, 1, 1, () => {
        r = null;
      }), vt());
      let m = t;
      t = c(_), t === m ? u[t].p(_, d) : (kt(), X(u[m], 1, 1, () => {
        u[m] = null;
      }), vt(), n = u[t], n ? n.p(_, d) : (n = u[t] = a[t](_), n.c()), j(n, 1), n.m(i.parentNode, i));
    },
    i(_) {
      o || (j(r), j(n), o = !0);
    },
    o(_) {
      X(r), X(n), o = !1;
    },
    d(_) {
      _ && (qe(e), qe(i)), r && r.d(_), u[t].d(_), s = !1, f();
    }
  };
}
function Fc(l, e, t) {
  let n, i, o;
  var s = this && this.__awaiter || function(S, W, G, ee) {
    function Q(ne) {
      return ne instanceof G ? ne : new G(function(Se) {
        Se(ne);
      });
    }
    return new (G || (G = Promise))(function(ne, Se) {
      function Tt(Ge) {
        try {
          xt(ee.next(Ge));
        } catch (ct) {
          Se(ct);
        }
      }
      function kn(Ge) {
        try {
          xt(ee.throw(Ge));
        } catch (ct) {
          Se(ct);
        }
      }
      function xt(Ge) {
        Ge.done ? ne(Ge.value) : Q(Ge.value).then(Tt, kn);
      }
      xt((ee = ee.apply(S, W || [])).next());
    });
  }, f, r, a;
  let { show_label: u = !0 } = e, { label: c } = e, { value: _ = null } = e, { columns: d = [2] } = e, { rows: m = void 0 } = e, { height: g = "auto" } = e, { preview: y } = e, { allow_preview: E = !0 } = e, { object_fit: k = "cover" } = e, { show_share_button: w = !1 } = e, { show_download_button: p = !1 } = e, { i18n: R } = e, { selected_index: b = null } = e, { interactive: F } = e, { _fetch: I } = e, { mode: D = "normal" } = e;
  const z = Dc();
  let C = !0, U = null, ie = _;
  b == null && y && (_ != null && _.length) && (b = 0);
  let J = b;
  function ce(S) {
    const W = S.target, G = S.offsetX, Q = W.offsetWidth / 2;
    G < Q ? t(0, b = n) : t(0, b = i);
  }
  function Z(S) {
    switch (S.code) {
      case "Escape":
        S.preventDefault(), t(0, b = null), z("unselect");
        break;
      case "ArrowLeft":
        S.preventDefault(), t(
          0,
          b = n
        );
        break;
      case "ArrowRight":
        S.preventDefault(), t(0, b = i);
        break;
    }
  }
  let te = [], oe;
  function Me(S) {
    return s(this, void 0, void 0, function* () {
      var W;
      if (typeof S != "number" || (yield Oc(), te[S] === void 0)) return;
      (W = te[S]) === null || W === void 0 || W.focus();
      const { left: G, width: ee } = oe.getBoundingClientRect(), { left: Q, width: ne } = te[S].getBoundingClientRect(), Tt = Q - G + ne / 2 - ee / 2 + oe.scrollLeft;
      oe && typeof oe.scrollTo == "function" && oe.scrollTo({
        left: Tt < 0 ? 0 : Tt,
        behavior: "smooth"
      });
    });
  }
  let _e = 0;
  function v(S, W) {
    return s(this, void 0, void 0, function* () {
      let G;
      try {
        G = yield I(S);
      } catch (Se) {
        if (Se instanceof TypeError) {
          window.open(S, "_blank", "noreferrer");
          return;
        }
        throw Se;
      }
      const ee = yield G.blob(), Q = URL.createObjectURL(ee), ne = document.createElement("a");
      ne.href = Q, ne.download = W, ne.click(), URL.revokeObjectURL(Q);
    });
  }
  function ke() {
    t(17, _e = Ba.innerHeight);
  }
  const V = () => {
    const S = o == null ? void 0 : o.image;
    if (S == null)
      return;
    const { url: W, orig_name: G } = S;
    W && v(W, G ?? "image");
  }, gt = () => {
    b !== null && (t(0, b = null), z("unselect"));
  }, L = (S) => ce(S);
  function We(S, W) {
    no[S ? "unshift" : "push"](() => {
      te[W] = S, t(15, te);
    });
  }
  const A = (S) => t(0, b = S);
  function B(S) {
    no[S ? "unshift" : "push"](() => {
      oe = S, t(16, oe);
    });
  }
  const K = () => {
    b !== null && (t(0, b = null), z("unselect"));
  };
  function $(S) {
    lo.call(this, l, S);
  }
  function ae(S) {
    lo.call(this, l, S);
  }
  const de = (S) => t(0, b = S);
  return l.$$set = (S) => {
    "show_label" in S && t(1, u = S.show_label), "label" in S && t(2, c = S.label), "value" in S && t(3, _ = S.value), "columns" in S && t(4, d = S.columns), "rows" in S && t(5, m = S.rows), "height" in S && t(6, g = S.height), "preview" in S && t(23, y = S.preview), "allow_preview" in S && t(7, E = S.allow_preview), "object_fit" in S && t(8, k = S.object_fit), "show_share_button" in S && t(9, w = S.show_share_button), "show_download_button" in S && t(10, p = S.show_download_button), "i18n" in S && t(11, R = S.i18n), "selected_index" in S && t(0, b = S.selected_index), "interactive" in S && t(12, F = S.interactive), "_fetch" in S && t(24, I = S._fetch), "mode" in S && t(13, D = S.mode);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value, was_reset*/
    268435464 && t(28, C = _ == null || _.length === 0 ? !0 : C), l.$$.dirty[0] & /*value*/
    8 && t(14, U = _ == null ? null : _.map((S) => ({ image: S.image, caption: S.caption }))), l.$$.dirty[0] & /*prev_value, value, was_reset, preview, selected_index*/
    813694985 && (cn(ie, _) || (C ? (t(0, b = y && (_ != null && _.length) ? 0 : null), t(28, C = !1)) : t(
      0,
      b = b != null && _ != null && b < _.length ? b : null
    ), z("change"), t(29, ie = _))), l.$$.dirty[0] & /*selected_index, resolved_value, _a, _b*/
    100679681 && (n = ((b ?? 0) + (t(25, f = U == null ? void 0 : U.length) !== null && f !== void 0 ? f : 0) - 1) % (t(26, r = U == null ? void 0 : U.length) !== null && r !== void 0 ? r : 0)), l.$$.dirty[0] & /*selected_index, resolved_value, _c*/
    134234113 && (i = ((b ?? 0) + 1) % (t(27, a = U == null ? void 0 : U.length) !== null && a !== void 0 ? a : 0)), l.$$.dirty[0] & /*selected_index, old_selected_index, resolved_value*/
    1073758209 && b !== J && (t(30, J = b), b !== null && z("select", {
      index: b,
      value: U == null ? void 0 : U[b]
    })), l.$$.dirty[0] & /*allow_preview, selected_index*/
    129 && E && Me(b), l.$$.dirty[0] & /*selected_index, resolved_value*/
    16385 && t(18, o = b != null && U != null ? U[b] : null);
  }, [
    b,
    u,
    c,
    _,
    d,
    m,
    g,
    E,
    k,
    w,
    p,
    R,
    F,
    D,
    U,
    te,
    oe,
    _e,
    o,
    z,
    ce,
    Z,
    v,
    y,
    I,
    f,
    r,
    a,
    C,
    ie,
    J,
    ke,
    V,
    gt,
    L,
    We,
    A,
    B,
    K,
    $,
    ae,
    de
  ];
}
class zc extends Ec {
  constructor(e) {
    super(), Cc(
      this,
      e,
      Fc,
      Pc,
      Rc,
      {
        show_label: 1,
        label: 2,
        value: 3,
        columns: 4,
        rows: 5,
        height: 6,
        preview: 23,
        allow_preview: 7,
        object_fit: 8,
        show_share_button: 9,
        show_download_button: 10,
        i18n: 11,
        selected_index: 0,
        interactive: 12,
        _fetch: 24,
        mode: 13
      },
      null,
      [-1, -1]
    );
  }
}
function Kt(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Bn() {
}
function Uc(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Ha = typeof window < "u";
let go = Ha ? () => window.performance.now() : () => Date.now(), ja = Ha ? (l) => requestAnimationFrame(l) : Bn;
const Jt = /* @__PURE__ */ new Set();
function Wa(l) {
  Jt.forEach((e) => {
    e.c(l) || (Jt.delete(e), e.f());
  }), Jt.size !== 0 && ja(Wa);
}
function qc(l) {
  let e;
  return Jt.size === 0 && ja(Wa), {
    promise: new Promise((t) => {
      Jt.add(e = { c: l, f: t });
    }),
    abort() {
      Jt.delete(e);
    }
  };
}
const Xt = [];
function Bc(l, e = Bn) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (Uc(l, f) && (l = f, t)) {
      const r = !Xt.length;
      for (const a of n)
        a[1](), Xt.push(a, l);
      if (r) {
        for (let a = 0; a < Xt.length; a += 2)
          Xt[a][0](Xt[a + 1]);
        Xt.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function s(f, r = Bn) {
    const a = [f, r];
    return n.add(a), n.size === 1 && (t = e(i, o) || Bn), f(l), () => {
      n.delete(a), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: s };
}
function po(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Vl(l, e, t, n) {
  if (typeof t == "number" || po(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, f = l.opts.damping * o, r = (s - f) * l.inv_mass, a = (o + r) * l.dt;
    return Math.abs(a) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, po(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => Vl(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = Vl(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function bo(l, e = {}) {
  const t = Bc(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let s, f, r, a = l, u = l, c = 1, _ = 0, d = !1;
  function m(y, E = {}) {
    u = y;
    const k = r = {};
    return l == null || E.hard || g.stiffness >= 1 && g.damping >= 1 ? (d = !0, s = go(), a = y, t.set(l = u), Promise.resolve()) : (E.soft && (_ = 1 / ((E.soft === !0 ? 0.5 : +E.soft) * 60), c = 0), f || (s = go(), d = !1, f = qc((w) => {
      if (d)
        return d = !1, f = null, !1;
      c = Math.min(c + _, 1);
      const p = {
        inv_mass: c,
        opts: g,
        settled: !0,
        dt: (w - s) * 60 / 1e3
      }, R = Vl(p, a, l, u);
      return s = w, a = l, t.set(l = R), p.settled && (f = null), !p.settled;
    })), new Promise((w) => {
      f.promise.then(() => {
        k === r && w();
      });
    }));
  }
  const g = {
    set: m,
    update: (y, E) => m(y(u, l), E),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return g;
}
const {
  SvelteComponent: Hc,
  append: Xe,
  attr: H,
  component_subscribe: wo,
  detach: jc,
  element: Wc,
  init: Gc,
  insert: Vc,
  noop: vo,
  safe_not_equal: Yc,
  set_style: On,
  svg_element: Ze,
  toggle_class: ko
} = window.__gradio__svelte__internal, { onMount: Xc } = window.__gradio__svelte__internal;
function Zc(l) {
  let e, t, n, i, o, s, f, r, a, u, c, _;
  return {
    c() {
      e = Wc("div"), t = Ze("svg"), n = Ze("g"), i = Ze("path"), o = Ze("path"), s = Ze("path"), f = Ze("path"), r = Ze("g"), a = Ze("path"), u = Ze("path"), c = Ze("path"), _ = Ze("path"), H(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), H(i, "fill", "#FF7C00"), H(i, "fill-opacity", "0.4"), H(i, "class", "svelte-43sxxs"), H(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), H(o, "fill", "#FF7C00"), H(o, "class", "svelte-43sxxs"), H(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), H(s, "fill", "#FF7C00"), H(s, "fill-opacity", "0.4"), H(s, "class", "svelte-43sxxs"), H(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), H(f, "fill", "#FF7C00"), H(f, "class", "svelte-43sxxs"), On(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), H(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), H(a, "fill", "#FF7C00"), H(a, "fill-opacity", "0.4"), H(a, "class", "svelte-43sxxs"), H(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), H(u, "fill", "#FF7C00"), H(u, "class", "svelte-43sxxs"), H(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), H(c, "fill", "#FF7C00"), H(c, "fill-opacity", "0.4"), H(c, "class", "svelte-43sxxs"), H(_, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), H(_, "fill", "#FF7C00"), H(_, "class", "svelte-43sxxs"), On(r, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), H(t, "viewBox", "-1200 -1200 3000 3000"), H(t, "fill", "none"), H(t, "xmlns", "http://www.w3.org/2000/svg"), H(t, "class", "svelte-43sxxs"), H(e, "class", "svelte-43sxxs"), ko(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(d, m) {
      Vc(d, e, m), Xe(e, t), Xe(t, n), Xe(n, i), Xe(n, o), Xe(n, s), Xe(n, f), Xe(t, r), Xe(r, a), Xe(r, u), Xe(r, c), Xe(r, _);
    },
    p(d, [m]) {
      m & /*$top*/
      2 && On(n, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), m & /*$bottom*/
      4 && On(r, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), m & /*margin*/
      1 && ko(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: vo,
    o: vo,
    d(d) {
      d && jc(e);
    }
  };
}
function Kc(l, e, t) {
  let n, i;
  var o = this && this.__awaiter || function(d, m, g, y) {
    function E(k) {
      return k instanceof g ? k : new g(function(w) {
        w(k);
      });
    }
    return new (g || (g = Promise))(function(k, w) {
      function p(F) {
        try {
          b(y.next(F));
        } catch (I) {
          w(I);
        }
      }
      function R(F) {
        try {
          b(y.throw(F));
        } catch (I) {
          w(I);
        }
      }
      function b(F) {
        F.done ? k(F.value) : E(F.value).then(p, R);
      }
      b((y = y.apply(d, m || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const f = bo([0, 0]);
  wo(l, f, (d) => t(1, n = d));
  const r = bo([0, 0]);
  wo(l, r, (d) => t(2, i = d));
  let a;
  function u() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), r.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), r.set([125, -140])]), yield Promise.all([f.set([-125, 0]), r.set([125, -0])]), yield Promise.all([f.set([125, 0]), r.set([-125, 0])]);
    });
  }
  function c() {
    return o(this, void 0, void 0, function* () {
      yield u(), a || c();
    });
  }
  function _() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), r.set([-125, 0])]), c();
    });
  }
  return Xc(() => (_(), () => a = !0)), l.$$set = (d) => {
    "margin" in d && t(0, s = d.margin);
  }, [s, n, i, f, r];
}
class Jc extends Hc {
  constructor(e) {
    super(), Gc(this, e, Kc, Zc, Yc, { margin: 0 });
  }
}
const {
  SvelteComponent: Qc,
  append: It,
  attr: $e,
  binding_callbacks: yo,
  check_outros: Yl,
  create_component: Ga,
  create_slot: Va,
  destroy_component: Ya,
  destroy_each: Xa,
  detach: N,
  element: at,
  empty: Qt,
  ensure_array_like: Zn,
  get_all_dirty_from_scope: Za,
  get_slot_changes: Ka,
  group_outros: Xl,
  init: xc,
  insert: P,
  mount_component: Ja,
  noop: Zl,
  safe_not_equal: $c,
  set_data: He,
  set_style: yt,
  space: Ue,
  text: x,
  toggle_class: Fe,
  transition_in: Qe,
  transition_out: rt,
  update_slot_base: Qa
} = window.__gradio__svelte__internal, { tick: e_ } = window.__gradio__svelte__internal, { onDestroy: t_ } = window.__gradio__svelte__internal, { createEventDispatcher: n_ } = window.__gradio__svelte__internal, l_ = (l) => ({}), Eo = (l) => ({}), i_ = (l) => ({}), To = (l) => ({});
function Ao(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function So(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function o_(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), s, f, r;
  t = new Bt({
    props: {
      Icon: ua,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const a = (
    /*#slots*/
    l[30].error
  ), u = Va(
    a,
    l,
    /*$$scope*/
    l[29],
    Eo
  );
  return {
    c() {
      e = at("div"), Ga(t.$$.fragment), n = Ue(), i = at("span"), s = x(o), f = Ue(), u && u.c(), $e(e, "class", "clear-status svelte-v0wucf"), $e(i, "class", "error svelte-v0wucf");
    },
    m(c, _) {
      P(c, e, _), Ja(t, e, null), P(c, n, _), P(c, i, _), It(i, s), P(c, f, _), u && u.m(c, _), r = !0;
    },
    p(c, _) {
      const d = {};
      _[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      c[1]("common.clear")), t.$set(d), (!r || _[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      c[1]("common.error") + "") && He(s, o), u && u.p && (!r || _[0] & /*$$scope*/
      536870912) && Qa(
        u,
        a,
        c,
        /*$$scope*/
        c[29],
        r ? Ka(
          a,
          /*$$scope*/
          c[29],
          _,
          l_
        ) : Za(
          /*$$scope*/
          c[29]
        ),
        Eo
      );
    },
    i(c) {
      r || (Qe(t.$$.fragment, c), Qe(u, c), r = !0);
    },
    o(c) {
      rt(t.$$.fragment, c), rt(u, c), r = !1;
    },
    d(c) {
      c && (N(e), N(n), N(i), N(f)), Ya(t), u && u.d(c);
    }
  };
}
function a_(l) {
  let e, t, n, i, o, s, f, r, a, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Co(l)
  );
  function c(w, p) {
    if (
      /*progress*/
      w[7]
    ) return f_;
    if (
      /*queue_position*/
      w[2] !== null && /*queue_size*/
      w[3] !== void 0 && /*queue_position*/
      w[2] >= 0
    ) return s_;
    if (
      /*queue_position*/
      w[2] === 0
    ) return r_;
  }
  let _ = c(l), d = _ && _(l), m = (
    /*timer*/
    l[5] && Do(l)
  );
  const g = [d_, __], y = [];
  function E(w, p) {
    return (
      /*last_progress_level*/
      w[15] != null ? 0 : (
        /*show_progress*/
        w[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = E(l)) && (s = y[o] = g[o](l));
  let k = !/*timer*/
  l[5] && zo(l);
  return {
    c() {
      u && u.c(), e = Ue(), t = at("div"), d && d.c(), n = Ue(), m && m.c(), i = Ue(), s && s.c(), f = Ue(), k && k.c(), r = Qt(), $e(t, "class", "progress-text svelte-v0wucf"), Fe(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), Fe(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(w, p) {
      u && u.m(w, p), P(w, e, p), P(w, t, p), d && d.m(t, null), It(t, n), m && m.m(t, null), P(w, i, p), ~o && y[o].m(w, p), P(w, f, p), k && k.m(w, p), P(w, r, p), a = !0;
    },
    p(w, p) {
      /*variant*/
      w[8] === "default" && /*show_eta_bar*/
      w[18] && /*show_progress*/
      w[6] === "full" ? u ? u.p(w, p) : (u = Co(w), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), _ === (_ = c(w)) && d ? d.p(w, p) : (d && d.d(1), d = _ && _(w), d && (d.c(), d.m(t, n))), /*timer*/
      w[5] ? m ? m.p(w, p) : (m = Do(w), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!a || p[0] & /*variant*/
      256) && Fe(
        t,
        "meta-text-center",
        /*variant*/
        w[8] === "center"
      ), (!a || p[0] & /*variant*/
      256) && Fe(
        t,
        "meta-text",
        /*variant*/
        w[8] === "default"
      );
      let R = o;
      o = E(w), o === R ? ~o && y[o].p(w, p) : (s && (Xl(), rt(y[R], 1, 1, () => {
        y[R] = null;
      }), Yl()), ~o ? (s = y[o], s ? s.p(w, p) : (s = y[o] = g[o](w), s.c()), Qe(s, 1), s.m(f.parentNode, f)) : s = null), /*timer*/
      w[5] ? k && (Xl(), rt(k, 1, 1, () => {
        k = null;
      }), Yl()) : k ? (k.p(w, p), p[0] & /*timer*/
      32 && Qe(k, 1)) : (k = zo(w), k.c(), Qe(k, 1), k.m(r.parentNode, r));
    },
    i(w) {
      a || (Qe(s), Qe(k), a = !0);
    },
    o(w) {
      rt(s), rt(k), a = !1;
    },
    d(w) {
      w && (N(e), N(t), N(i), N(f), N(r)), u && u.d(w), d && d.d(), m && m.d(), ~o && y[o].d(w), k && k.d(w);
    }
  };
}
function Co(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = at("div"), $e(e, "class", "eta-bar svelte-v0wucf"), yt(e, "transform", t);
    },
    m(n, i) {
      P(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && yt(e, "transform", t);
    },
    d(n) {
      n && N(e);
    }
  };
}
function r_(l) {
  let e;
  return {
    c() {
      e = x("processing |");
    },
    m(t, n) {
      P(t, e, n);
    },
    p: Zl,
    d(t) {
      t && N(e);
    }
  };
}
function s_(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, s;
  return {
    c() {
      e = x("queue: "), n = x(t), i = x("/"), o = x(
        /*queue_size*/
        l[3]
      ), s = x(" |");
    },
    m(f, r) {
      P(f, e, r), P(f, n, r), P(f, i, r), P(f, o, r), P(f, s, r);
    },
    p(f, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && He(n, t), r[0] & /*queue_size*/
      8 && He(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (N(e), N(n), N(i), N(o), N(s));
    }
  };
}
function f_(l) {
  let e, t = Zn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Ro(So(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Qt();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      P(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Zn(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = So(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = Ro(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && N(e), Xa(n, i);
    }
  };
}
function Lo(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, o = " ", s;
  function f(u, c) {
    return (
      /*p*/
      u[41].length != null ? c_ : u_
    );
  }
  let r = f(l), a = r(l);
  return {
    c() {
      a.c(), e = Ue(), n = x(t), i = x(" | "), s = x(o);
    },
    m(u, c) {
      a.m(u, c), P(u, e, c), P(u, n, c), P(u, i, c), P(u, s, c);
    },
    p(u, c) {
      r === (r = f(u)) && a ? a.p(u, c) : (a.d(1), a = r(u), a && (a.c(), a.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && He(n, t);
    },
    d(u) {
      u && (N(e), N(n), N(i), N(s)), a.d(u);
    }
  };
}
function u_(l) {
  let e = Kt(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = x(e);
    },
    m(n, i) {
      P(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Kt(
        /*p*/
        n[41].index || 0
      ) + "") && He(t, e);
    },
    d(n) {
      n && N(t);
    }
  };
}
function c_(l) {
  let e = Kt(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = Kt(
    /*p*/
    l[41].length
  ) + "", o;
  return {
    c() {
      t = x(e), n = x("/"), o = x(i);
    },
    m(s, f) {
      P(s, t, f), P(s, n, f), P(s, o, f);
    },
    p(s, f) {
      f[0] & /*progress*/
      128 && e !== (e = Kt(
        /*p*/
        s[41].index || 0
      ) + "") && He(t, e), f[0] & /*progress*/
      128 && i !== (i = Kt(
        /*p*/
        s[41].length
      ) + "") && He(o, i);
    },
    d(s) {
      s && (N(t), N(n), N(o));
    }
  };
}
function Ro(l) {
  let e, t = (
    /*p*/
    l[41].index != null && Lo(l)
  );
  return {
    c() {
      t && t.c(), e = Qt();
    },
    m(n, i) {
      t && t.m(n, i), P(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = Lo(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && N(e), t && t.d(n);
    }
  };
}
function Do(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = x(
        /*formatted_timer*/
        l[20]
      ), n = x(t), i = x("s");
    },
    m(o, s) {
      P(o, e, s), P(o, n, s), P(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && He(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && He(n, t);
    },
    d(o) {
      o && (N(e), N(n), N(i));
    }
  };
}
function __(l) {
  let e, t;
  return e = new Jc({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Ga(e.$$.fragment);
    },
    m(n, i) {
      Ja(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (Qe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      rt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ya(e, n);
    }
  };
}
function d_(l) {
  let e, t, n, i, o, s = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && Oo(l)
  );
  return {
    c() {
      e = at("div"), t = at("div"), f && f.c(), n = Ue(), i = at("div"), o = at("div"), $e(t, "class", "progress-level-inner svelte-v0wucf"), $e(o, "class", "progress-bar svelte-v0wucf"), yt(o, "width", s), $e(i, "class", "progress-bar-wrap svelte-v0wucf"), $e(e, "class", "progress-level svelte-v0wucf");
    },
    m(r, a) {
      P(r, e, a), It(e, t), f && f.m(t, null), It(e, n), It(e, i), It(i, o), l[31](o);
    },
    p(r, a) {
      /*progress*/
      r[7] != null ? f ? f.p(r, a) : (f = Oo(r), f.c(), f.m(t, null)) : f && (f.d(1), f = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      r[15] * 100}%`) && yt(o, "width", s);
    },
    i: Zl,
    o: Zl,
    d(r) {
      r && N(e), f && f.d(), l[31](null);
    }
  };
}
function Oo(l) {
  let e, t = Zn(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Fo(Ao(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Qt();
    },
    m(i, o) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, o);
      P(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Zn(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const f = Ao(i, t, s);
          n[s] ? n[s].p(f, o) : (n[s] = Fo(f), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && N(e), Xa(n, i);
    }
  };
}
function Io(l) {
  let e, t, n, i, o = (
    /*i*/
    l[43] !== 0 && m_()
  ), s = (
    /*p*/
    l[41].desc != null && Mo(l)
  ), f = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && No()
  ), r = (
    /*progress_level*/
    l[14] != null && Po(l)
  );
  return {
    c() {
      o && o.c(), e = Ue(), s && s.c(), t = Ue(), f && f.c(), n = Ue(), r && r.c(), i = Qt();
    },
    m(a, u) {
      o && o.m(a, u), P(a, e, u), s && s.m(a, u), P(a, t, u), f && f.m(a, u), P(a, n, u), r && r.m(a, u), P(a, i, u);
    },
    p(a, u) {
      /*p*/
      a[41].desc != null ? s ? s.p(a, u) : (s = Mo(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? f || (f = No(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      a[14] != null ? r ? r.p(a, u) : (r = Po(a), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(a) {
      a && (N(e), N(t), N(n), N(i)), o && o.d(a), s && s.d(a), f && f.d(a), r && r.d(a);
    }
  };
}
function m_(l) {
  let e;
  return {
    c() {
      e = x(" /");
    },
    m(t, n) {
      P(t, e, n);
    },
    d(t) {
      t && N(e);
    }
  };
}
function Mo(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = x(e);
    },
    m(n, i) {
      P(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && He(t, e);
    },
    d(n) {
      n && N(t);
    }
  };
}
function No(l) {
  let e;
  return {
    c() {
      e = x("-");
    },
    m(t, n) {
      P(t, e, n);
    },
    d(t) {
      t && N(e);
    }
  };
}
function Po(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = x(e), n = x("%");
    },
    m(i, o) {
      P(i, t, o), P(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && He(t, e);
    },
    d(i) {
      i && (N(t), N(n));
    }
  };
}
function Fo(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && Io(l)
  );
  return {
    c() {
      t && t.c(), e = Qt();
    },
    m(n, i) {
      t && t.m(n, i), P(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = Io(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && N(e), t && t.d(n);
    }
  };
}
function zo(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), s = Va(
    o,
    l,
    /*$$scope*/
    l[29],
    To
  );
  return {
    c() {
      e = at("p"), t = x(
        /*loading_text*/
        l[9]
      ), n = Ue(), s && s.c(), $e(e, "class", "loading svelte-v0wucf");
    },
    m(f, r) {
      P(f, e, r), It(e, t), P(f, n, r), s && s.m(f, r), i = !0;
    },
    p(f, r) {
      (!i || r[0] & /*loading_text*/
      512) && He(
        t,
        /*loading_text*/
        f[9]
      ), s && s.p && (!i || r[0] & /*$$scope*/
      536870912) && Qa(
        s,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Ka(
          o,
          /*$$scope*/
          f[29],
          r,
          i_
        ) : Za(
          /*$$scope*/
          f[29]
        ),
        To
      );
    },
    i(f) {
      i || (Qe(s, f), i = !0);
    },
    o(f) {
      rt(s, f), i = !1;
    },
    d(f) {
      f && (N(e), N(n)), s && s.d(f);
    }
  };
}
function h_(l) {
  let e, t, n, i, o;
  const s = [a_, o_], f = [];
  function r(a, u) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(l)) && (n = f[t] = s[t](l)), {
    c() {
      e = at("div"), n && n.c(), $e(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-v0wucf"), Fe(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), Fe(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), Fe(
        e,
        "generating",
        /*status*/
        l[4] === "generating" && /*show_progress*/
        l[6] === "full"
      ), Fe(
        e,
        "border",
        /*border*/
        l[12]
      ), yt(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), yt(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, u) {
      P(a, e, u), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(a, u) {
      let c = t;
      t = r(a), t === c ? ~t && f[t].p(a, u) : (n && (Xl(), rt(f[c], 1, 1, () => {
        f[c] = null;
      }), Yl()), ~t ? (n = f[t], n ? n.p(a, u) : (n = f[t] = s[t](a), n.c()), Qe(n, 1), n.m(e, null)) : n = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-v0wucf")) && $e(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && Fe(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && Fe(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && Fe(
        e,
        "generating",
        /*status*/
        a[4] === "generating" && /*show_progress*/
        a[6] === "full"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && Fe(
        e,
        "border",
        /*border*/
        a[12]
      ), u[0] & /*absolute*/
      1024 && yt(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && yt(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      o || (Qe(n), o = !0);
    },
    o(a) {
      rt(n), o = !1;
    },
    d(a) {
      a && N(e), ~t && f[t].d(), l[33](null);
    }
  };
}
var g_ = function(l, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function f(u) {
      try {
        a(n.next(u));
      } catch (c) {
        s(c);
      }
    }
    function r(u) {
      try {
        a(n.throw(u));
      } catch (c) {
        s(c);
      }
    }
    function a(u) {
      u.done ? o(u.value) : i(u.value).then(f, r);
    }
    a((n = n.apply(l, e || [])).next());
  });
};
let In = [], Dl = !1;
function p_(l) {
  return g_(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (In.push(e), !Dl) Dl = !0;
      else return;
      yield e_(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < In.length; i++) {
          const s = In[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= n[0]) && (n[0] = s.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Dl = !1, In = [];
      });
    }
  });
}
function b_(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  const s = n_();
  let { i18n: f } = e, { eta: r = null } = e, { queue_position: a } = e, { queue_size: u } = e, { status: c } = e, { scroll_to_output: _ = !1 } = e, { timer: d = !0 } = e, { show_progress: m = "full" } = e, { message: g = null } = e, { progress: y = null } = e, { variant: E = "default" } = e, { loading_text: k = "Loading..." } = e, { absolute: w = !0 } = e, { translucent: p = !1 } = e, { border: R = !1 } = e, { autoscroll: b } = e, F, I = !1, D = 0, z = 0, C = null, U = null, ie = 0, J = null, ce, Z = null, te = !0;
  const oe = () => {
    t(0, r = t(27, C = t(19, v = null))), t(25, D = performance.now()), t(26, z = 0), I = !0, Me();
  };
  function Me() {
    requestAnimationFrame(() => {
      t(26, z = (performance.now() - D) / 1e3), I && Me();
    });
  }
  function _e() {
    t(26, z = 0), t(0, r = t(27, C = t(19, v = null))), I && (I = !1);
  }
  t_(() => {
    I && _e();
  });
  let v = null;
  function ke(L) {
    yo[L ? "unshift" : "push"](() => {
      Z = L, t(16, Z), t(7, y), t(14, J), t(15, ce);
    });
  }
  const V = () => {
    s("clear_status");
  };
  function gt(L) {
    yo[L ? "unshift" : "push"](() => {
      F = L, t(13, F);
    });
  }
  return l.$$set = (L) => {
    "i18n" in L && t(1, f = L.i18n), "eta" in L && t(0, r = L.eta), "queue_position" in L && t(2, a = L.queue_position), "queue_size" in L && t(3, u = L.queue_size), "status" in L && t(4, c = L.status), "scroll_to_output" in L && t(22, _ = L.scroll_to_output), "timer" in L && t(5, d = L.timer), "show_progress" in L && t(6, m = L.show_progress), "message" in L && t(23, g = L.message), "progress" in L && t(7, y = L.progress), "variant" in L && t(8, E = L.variant), "loading_text" in L && t(9, k = L.loading_text), "absolute" in L && t(10, w = L.absolute), "translucent" in L && t(11, p = L.translucent), "border" in L && t(12, R = L.border), "autoscroll" in L && t(24, b = L.autoscroll), "$$scope" in L && t(29, o = L.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (r === null && t(0, r = C), r != null && C !== r && (t(28, U = (performance.now() - D) / 1e3 + r), t(19, v = U.toFixed(1)), t(27, C = r))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ie = U === null || U <= 0 || !z ? null : Math.min(z / U, 1)), l.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, te = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, J = y.map((L) => {
      if (L.index != null && L.length != null)
        return L.index / L.length;
      if (L.progress != null)
        return L.progress;
    })) : t(14, J = null), J ? (t(15, ce = J[J.length - 1]), Z && (ce === 0 ? t(16, Z.style.transition = "0", Z) : t(16, Z.style.transition = "150ms", Z))) : t(15, ce = void 0)), l.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? oe() : _e()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && F && _ && (c === "pending" || c === "complete") && p_(F, b), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = z.toFixed(1));
  }, [
    r,
    f,
    a,
    u,
    c,
    d,
    m,
    y,
    E,
    k,
    w,
    p,
    R,
    F,
    J,
    ce,
    Z,
    ie,
    te,
    v,
    n,
    s,
    _,
    g,
    b,
    D,
    z,
    C,
    U,
    o,
    i,
    ke,
    V,
    gt
  ];
}
class w_ extends Qc {
  constructor(e) {
    super(), xc(
      this,
      e,
      b_,
      h_,
      $c,
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
  entries: xa,
  setPrototypeOf: Uo,
  isFrozen: v_,
  getPrototypeOf: k_,
  getOwnPropertyDescriptor: y_
} = Object;
let {
  freeze: ve,
  seal: je,
  create: $a
} = Object, {
  apply: Kl,
  construct: Jl
} = typeof Reflect < "u" && Reflect;
ve || (ve = function(e) {
  return e;
});
je || (je = function(e) {
  return e;
});
Kl || (Kl = function(e, t, n) {
  return e.apply(t, n);
});
Jl || (Jl = function(e, t) {
  return new e(...t);
});
const Mn = Ie(Array.prototype.forEach), qo = Ie(Array.prototype.pop), ln = Ie(Array.prototype.push), Hn = Ie(String.prototype.toLowerCase), Ol = Ie(String.prototype.toString), Bo = Ie(String.prototype.match), on = Ie(String.prototype.replace), E_ = Ie(String.prototype.indexOf), T_ = Ie(String.prototype.trim), Ke = Ie(Object.prototype.hasOwnProperty), be = Ie(RegExp.prototype.test), an = A_(TypeError);
function Ie(l) {
  return function(e) {
    for (var t = arguments.length, n = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
      n[i - 1] = arguments[i];
    return Kl(l, e, n);
  };
}
function A_(l) {
  return function() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
      t[n] = arguments[n];
    return Jl(l, t);
  };
}
function q(l, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : Hn;
  Uo && Uo(l, null);
  let n = e.length;
  for (; n--; ) {
    let i = e[n];
    if (typeof i == "string") {
      const o = t(i);
      o !== i && (v_(e) || (e[n] = o), i = o);
    }
    l[i] = !0;
  }
  return l;
}
function S_(l) {
  for (let e = 0; e < l.length; e++)
    Ke(l, e) || (l[e] = null);
  return l;
}
function Lt(l) {
  const e = $a(null);
  for (const [t, n] of xa(l))
    Ke(l, t) && (Array.isArray(n) ? e[t] = S_(n) : n && typeof n == "object" && n.constructor === Object ? e[t] = Lt(n) : e[t] = n);
  return e;
}
function rn(l, e) {
  for (; l !== null; ) {
    const n = y_(l, e);
    if (n) {
      if (n.get)
        return Ie(n.get);
      if (typeof n.value == "function")
        return Ie(n.value);
    }
    l = k_(l);
  }
  function t() {
    return null;
  }
  return t;
}
const Ho = ve(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), Il = ve(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), Ml = ve(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), C_ = ve(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), Nl = ve(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), L_ = ve(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), jo = ve(["#text"]), Wo = ve(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), Pl = ve(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), Go = ve(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Nn = ve(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), R_ = je(/\{\{[\w\W]*|[\w\W]*\}\}/gm), D_ = je(/<%[\w\W]*|[\w\W]*%>/gm), O_ = je(/\${[\w\W]*}/gm), I_ = je(/^data-[\-\w.\u00B7-\uFFFF]/), M_ = je(/^aria-[\-\w]+$/), er = je(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), N_ = je(/^(?:\w+script|data):/i), P_ = je(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), tr = je(/^html$/i), F_ = je(/^[a-z][.\w]*(-[.\w]+)+$/i);
var Vo = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR: R_,
  ERB_EXPR: D_,
  TMPLIT_EXPR: O_,
  DATA_ATTR: I_,
  ARIA_ATTR: M_,
  IS_ALLOWED_URI: er,
  IS_SCRIPT_OR_DATA: N_,
  ATTR_WHITESPACE: P_,
  DOCTYPE_NAME: tr,
  CUSTOM_ELEMENT: F_
});
const sn = {
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
}, z_ = function() {
  return typeof window > "u" ? null : window;
}, U_ = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let n = null;
  const i = "data-tt-policy-suffix";
  t && t.hasAttribute(i) && (n = t.getAttribute(i));
  const o = "dompurify" + (n ? "#" + n : "");
  try {
    return e.createPolicy(o, {
      createHTML(s) {
        return s;
      },
      createScriptURL(s) {
        return s;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function nr() {
  let l = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : z_();
  const e = (M) => nr(M);
  if (e.version = "3.1.6", e.removed = [], !l || !l.document || l.document.nodeType !== sn.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = l;
  const n = t, i = n.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: s,
    Node: f,
    Element: r,
    NodeFilter: a,
    NamedNodeMap: u = l.NamedNodeMap || l.MozNamedAttrMap,
    HTMLFormElement: c,
    DOMParser: _,
    trustedTypes: d
  } = l, m = r.prototype, g = rn(m, "cloneNode"), y = rn(m, "remove"), E = rn(m, "nextSibling"), k = rn(m, "childNodes"), w = rn(m, "parentNode");
  if (typeof s == "function") {
    const M = t.createElement("template");
    M.content && M.content.ownerDocument && (t = M.content.ownerDocument);
  }
  let p, R = "";
  const {
    implementation: b,
    createNodeIterator: F,
    createDocumentFragment: I,
    getElementsByTagName: D
  } = t, {
    importNode: z
  } = n;
  let C = {};
  e.isSupported = typeof xa == "function" && typeof w == "function" && b && b.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: U,
    ERB_EXPR: ie,
    TMPLIT_EXPR: J,
    DATA_ATTR: ce,
    ARIA_ATTR: Z,
    IS_SCRIPT_OR_DATA: te,
    ATTR_WHITESPACE: oe,
    CUSTOM_ELEMENT: Me
  } = Vo;
  let {
    IS_ALLOWED_URI: _e
  } = Vo, v = null;
  const ke = q({}, [...Ho, ...Il, ...Ml, ...Nl, ...jo]);
  let V = null;
  const gt = q({}, [...Wo, ...Pl, ...Go, ...Nn]);
  let L = Object.seal($a(null, {
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
  })), We = null, A = null, B = !0, K = !0, $ = !1, ae = !0, de = !1, S = !0, W = !1, G = !1, ee = !1, Q = !1, ne = !1, Se = !1, Tt = !0, kn = !1;
  const xt = "user-content-";
  let Ge = !0, ct = !1, Ht = {}, jt = null;
  const ri = q({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let si = null;
  const fi = q({}, ["audio", "video", "img", "source", "image", "track"]);
  let ol = null;
  const ui = q({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), yn = "http://www.w3.org/1998/Math/MathML", En = "http://www.w3.org/2000/svg", _t = "http://www.w3.org/1999/xhtml";
  let Wt = _t, al = !1, rl = null;
  const ar = q({}, [yn, En, _t], Ol);
  let $t = null;
  const rr = ["application/xhtml+xml", "text/html"], sr = "text/html";
  let se = null, Gt = null;
  const fr = t.createElement("form"), ci = function(h) {
    return h instanceof RegExp || h instanceof Function;
  }, sl = function() {
    let h = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(Gt && Gt === h)) {
      if ((!h || typeof h != "object") && (h = {}), h = Lt(h), $t = // eslint-disable-next-line unicorn/prefer-includes
      rr.indexOf(h.PARSER_MEDIA_TYPE) === -1 ? sr : h.PARSER_MEDIA_TYPE, se = $t === "application/xhtml+xml" ? Ol : Hn, v = Ke(h, "ALLOWED_TAGS") ? q({}, h.ALLOWED_TAGS, se) : ke, V = Ke(h, "ALLOWED_ATTR") ? q({}, h.ALLOWED_ATTR, se) : gt, rl = Ke(h, "ALLOWED_NAMESPACES") ? q({}, h.ALLOWED_NAMESPACES, Ol) : ar, ol = Ke(h, "ADD_URI_SAFE_ATTR") ? q(
        Lt(ui),
        // eslint-disable-line indent
        h.ADD_URI_SAFE_ATTR,
        // eslint-disable-line indent
        se
        // eslint-disable-line indent
      ) : ui, si = Ke(h, "ADD_DATA_URI_TAGS") ? q(
        Lt(fi),
        // eslint-disable-line indent
        h.ADD_DATA_URI_TAGS,
        // eslint-disable-line indent
        se
        // eslint-disable-line indent
      ) : fi, jt = Ke(h, "FORBID_CONTENTS") ? q({}, h.FORBID_CONTENTS, se) : ri, We = Ke(h, "FORBID_TAGS") ? q({}, h.FORBID_TAGS, se) : {}, A = Ke(h, "FORBID_ATTR") ? q({}, h.FORBID_ATTR, se) : {}, Ht = Ke(h, "USE_PROFILES") ? h.USE_PROFILES : !1, B = h.ALLOW_ARIA_ATTR !== !1, K = h.ALLOW_DATA_ATTR !== !1, $ = h.ALLOW_UNKNOWN_PROTOCOLS || !1, ae = h.ALLOW_SELF_CLOSE_IN_ATTR !== !1, de = h.SAFE_FOR_TEMPLATES || !1, S = h.SAFE_FOR_XML !== !1, W = h.WHOLE_DOCUMENT || !1, Q = h.RETURN_DOM || !1, ne = h.RETURN_DOM_FRAGMENT || !1, Se = h.RETURN_TRUSTED_TYPE || !1, ee = h.FORCE_BODY || !1, Tt = h.SANITIZE_DOM !== !1, kn = h.SANITIZE_NAMED_PROPS || !1, Ge = h.KEEP_CONTENT !== !1, ct = h.IN_PLACE || !1, _e = h.ALLOWED_URI_REGEXP || er, Wt = h.NAMESPACE || _t, L = h.CUSTOM_ELEMENT_HANDLING || {}, h.CUSTOM_ELEMENT_HANDLING && ci(h.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (L.tagNameCheck = h.CUSTOM_ELEMENT_HANDLING.tagNameCheck), h.CUSTOM_ELEMENT_HANDLING && ci(h.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (L.attributeNameCheck = h.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), h.CUSTOM_ELEMENT_HANDLING && typeof h.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (L.allowCustomizedBuiltInElements = h.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), de && (K = !1), ne && (Q = !0), Ht && (v = q({}, jo), V = [], Ht.html === !0 && (q(v, Ho), q(V, Wo)), Ht.svg === !0 && (q(v, Il), q(V, Pl), q(V, Nn)), Ht.svgFilters === !0 && (q(v, Ml), q(V, Pl), q(V, Nn)), Ht.mathMl === !0 && (q(v, Nl), q(V, Go), q(V, Nn))), h.ADD_TAGS && (v === ke && (v = Lt(v)), q(v, h.ADD_TAGS, se)), h.ADD_ATTR && (V === gt && (V = Lt(V)), q(V, h.ADD_ATTR, se)), h.ADD_URI_SAFE_ATTR && q(ol, h.ADD_URI_SAFE_ATTR, se), h.FORBID_CONTENTS && (jt === ri && (jt = Lt(jt)), q(jt, h.FORBID_CONTENTS, se)), Ge && (v["#text"] = !0), W && q(v, ["html", "head", "body"]), v.table && (q(v, ["tbody"]), delete We.tbody), h.TRUSTED_TYPES_POLICY) {
        if (typeof h.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw an('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof h.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw an('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        p = h.TRUSTED_TYPES_POLICY, R = p.createHTML("");
      } else
        p === void 0 && (p = U_(d, i)), p !== null && typeof R == "string" && (R = p.createHTML(""));
      ve && ve(h), Gt = h;
    }
  }, _i = q({}, ["mi", "mo", "mn", "ms", "mtext"]), di = q({}, ["foreignobject", "annotation-xml"]), ur = q({}, ["title", "style", "font", "a", "script"]), mi = q({}, [...Il, ...Ml, ...C_]), hi = q({}, [...Nl, ...L_]), cr = function(h) {
    let T = w(h);
    (!T || !T.tagName) && (T = {
      namespaceURI: Wt,
      tagName: "template"
    });
    const O = Hn(h.tagName), Y = Hn(T.tagName);
    return rl[h.namespaceURI] ? h.namespaceURI === En ? T.namespaceURI === _t ? O === "svg" : T.namespaceURI === yn ? O === "svg" && (Y === "annotation-xml" || _i[Y]) : !!mi[O] : h.namespaceURI === yn ? T.namespaceURI === _t ? O === "math" : T.namespaceURI === En ? O === "math" && di[Y] : !!hi[O] : h.namespaceURI === _t ? T.namespaceURI === En && !di[Y] || T.namespaceURI === yn && !_i[Y] ? !1 : !hi[O] && (ur[O] || !mi[O]) : !!($t === "application/xhtml+xml" && rl[h.namespaceURI]) : !1;
  }, et = function(h) {
    ln(e.removed, {
      element: h
    });
    try {
      w(h).removeChild(h);
    } catch {
      y(h);
    }
  }, Tn = function(h, T) {
    try {
      ln(e.removed, {
        attribute: T.getAttributeNode(h),
        from: T
      });
    } catch {
      ln(e.removed, {
        attribute: null,
        from: T
      });
    }
    if (T.removeAttribute(h), h === "is" && !V[h])
      if (Q || ne)
        try {
          et(T);
        } catch {
        }
      else
        try {
          T.setAttribute(h, "");
        } catch {
        }
  }, gi = function(h) {
    let T = null, O = null;
    if (ee)
      h = "<remove></remove>" + h;
    else {
      const ue = Bo(h, /^[\r\n\t ]+/);
      O = ue && ue[0];
    }
    $t === "application/xhtml+xml" && Wt === _t && (h = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + h + "</body></html>");
    const Y = p ? p.createHTML(h) : h;
    if (Wt === _t)
      try {
        T = new _().parseFromString(Y, $t);
      } catch {
      }
    if (!T || !T.documentElement) {
      T = b.createDocument(Wt, "template", null);
      try {
        T.documentElement.innerHTML = al ? R : Y;
      } catch {
      }
    }
    const me = T.body || T.documentElement;
    return h && O && me.insertBefore(t.createTextNode(O), me.childNodes[0] || null), Wt === _t ? D.call(T, W ? "html" : "body")[0] : W ? T.documentElement : me;
  }, pi = function(h) {
    return F.call(
      h.ownerDocument || h,
      h,
      // eslint-disable-next-line no-bitwise
      a.SHOW_ELEMENT | a.SHOW_COMMENT | a.SHOW_TEXT | a.SHOW_PROCESSING_INSTRUCTION | a.SHOW_CDATA_SECTION,
      null
    );
  }, bi = function(h) {
    return h instanceof c && (typeof h.nodeName != "string" || typeof h.textContent != "string" || typeof h.removeChild != "function" || !(h.attributes instanceof u) || typeof h.removeAttribute != "function" || typeof h.setAttribute != "function" || typeof h.namespaceURI != "string" || typeof h.insertBefore != "function" || typeof h.hasChildNodes != "function");
  }, wi = function(h) {
    return typeof f == "function" && h instanceof f;
  }, dt = function(h, T, O) {
    C[h] && Mn(C[h], (Y) => {
      Y.call(e, T, O, Gt);
    });
  }, vi = function(h) {
    let T = null;
    if (dt("beforeSanitizeElements", h, null), bi(h))
      return et(h), !0;
    const O = se(h.nodeName);
    if (dt("uponSanitizeElement", h, {
      tagName: O,
      allowedTags: v
    }), h.hasChildNodes() && !wi(h.firstElementChild) && be(/<[/\w]/g, h.innerHTML) && be(/<[/\w]/g, h.textContent) || h.nodeType === sn.progressingInstruction || S && h.nodeType === sn.comment && be(/<[/\w]/g, h.data))
      return et(h), !0;
    if (!v[O] || We[O]) {
      if (!We[O] && yi(O) && (L.tagNameCheck instanceof RegExp && be(L.tagNameCheck, O) || L.tagNameCheck instanceof Function && L.tagNameCheck(O)))
        return !1;
      if (Ge && !jt[O]) {
        const Y = w(h) || h.parentNode, me = k(h) || h.childNodes;
        if (me && Y) {
          const ue = me.length;
          for (let ye = ue - 1; ye >= 0; --ye) {
            const tt = g(me[ye], !0);
            tt.__removalCount = (h.__removalCount || 0) + 1, Y.insertBefore(tt, E(h));
          }
        }
      }
      return et(h), !0;
    }
    return h instanceof r && !cr(h) || (O === "noscript" || O === "noembed" || O === "noframes") && be(/<\/no(script|embed|frames)/i, h.innerHTML) ? (et(h), !0) : (de && h.nodeType === sn.text && (T = h.textContent, Mn([U, ie, J], (Y) => {
      T = on(T, Y, " ");
    }), h.textContent !== T && (ln(e.removed, {
      element: h.cloneNode()
    }), h.textContent = T)), dt("afterSanitizeElements", h, null), !1);
  }, ki = function(h, T, O) {
    if (Tt && (T === "id" || T === "name") && (O in t || O in fr))
      return !1;
    if (!(K && !A[T] && be(ce, T))) {
      if (!(B && be(Z, T))) {
        if (!V[T] || A[T]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(yi(h) && (L.tagNameCheck instanceof RegExp && be(L.tagNameCheck, h) || L.tagNameCheck instanceof Function && L.tagNameCheck(h)) && (L.attributeNameCheck instanceof RegExp && be(L.attributeNameCheck, T) || L.attributeNameCheck instanceof Function && L.attributeNameCheck(T)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            T === "is" && L.allowCustomizedBuiltInElements && (L.tagNameCheck instanceof RegExp && be(L.tagNameCheck, O) || L.tagNameCheck instanceof Function && L.tagNameCheck(O)))
          ) return !1;
        } else if (!ol[T]) {
          if (!be(_e, on(O, oe, ""))) {
            if (!((T === "src" || T === "xlink:href" || T === "href") && h !== "script" && E_(O, "data:") === 0 && si[h])) {
              if (!($ && !be(te, on(O, oe, "")))) {
                if (O)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, yi = function(h) {
    return h !== "annotation-xml" && Bo(h, Me);
  }, Ei = function(h) {
    dt("beforeSanitizeAttributes", h, null);
    const {
      attributes: T
    } = h;
    if (!T)
      return;
    const O = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: V
    };
    let Y = T.length;
    for (; Y--; ) {
      const me = T[Y], {
        name: ue,
        namespaceURI: ye,
        value: tt
      } = me, en = se(ue);
      let pe = ue === "value" ? tt : T_(tt);
      if (O.attrName = en, O.attrValue = pe, O.keepAttr = !0, O.forceKeepAttr = void 0, dt("uponSanitizeAttribute", h, O), pe = O.attrValue, S && be(/((--!?|])>)|<\/(style|title)/i, pe)) {
        Tn(ue, h);
        continue;
      }
      if (O.forceKeepAttr || (Tn(ue, h), !O.keepAttr))
        continue;
      if (!ae && be(/\/>/i, pe)) {
        Tn(ue, h);
        continue;
      }
      de && Mn([U, ie, J], (Ai) => {
        pe = on(pe, Ai, " ");
      });
      const Ti = se(h.nodeName);
      if (ki(Ti, en, pe)) {
        if (kn && (en === "id" || en === "name") && (Tn(ue, h), pe = xt + pe), p && typeof d == "object" && typeof d.getAttributeType == "function" && !ye)
          switch (d.getAttributeType(Ti, en)) {
            case "TrustedHTML": {
              pe = p.createHTML(pe);
              break;
            }
            case "TrustedScriptURL": {
              pe = p.createScriptURL(pe);
              break;
            }
          }
        try {
          ye ? h.setAttributeNS(ye, ue, pe) : h.setAttribute(ue, pe), bi(h) ? et(h) : qo(e.removed);
        } catch {
        }
      }
    }
    dt("afterSanitizeAttributes", h, null);
  }, _r = function M(h) {
    let T = null;
    const O = pi(h);
    for (dt("beforeSanitizeShadowDOM", h, null); T = O.nextNode(); )
      dt("uponSanitizeShadowNode", T, null), !vi(T) && (T.content instanceof o && M(T.content), Ei(T));
    dt("afterSanitizeShadowDOM", h, null);
  };
  return e.sanitize = function(M) {
    let h = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, T = null, O = null, Y = null, me = null;
    if (al = !M, al && (M = "<!-->"), typeof M != "string" && !wi(M))
      if (typeof M.toString == "function") {
        if (M = M.toString(), typeof M != "string")
          throw an("dirty is not a string, aborting");
      } else
        throw an("toString is not a function");
    if (!e.isSupported)
      return M;
    if (G || sl(h), e.removed = [], typeof M == "string" && (ct = !1), ct) {
      if (M.nodeName) {
        const tt = se(M.nodeName);
        if (!v[tt] || We[tt])
          throw an("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (M instanceof f)
      T = gi("<!---->"), O = T.ownerDocument.importNode(M, !0), O.nodeType === sn.element && O.nodeName === "BODY" || O.nodeName === "HTML" ? T = O : T.appendChild(O);
    else {
      if (!Q && !de && !W && // eslint-disable-next-line unicorn/prefer-includes
      M.indexOf("<") === -1)
        return p && Se ? p.createHTML(M) : M;
      if (T = gi(M), !T)
        return Q ? null : Se ? R : "";
    }
    T && ee && et(T.firstChild);
    const ue = pi(ct ? M : T);
    for (; Y = ue.nextNode(); )
      vi(Y) || (Y.content instanceof o && _r(Y.content), Ei(Y));
    if (ct)
      return M;
    if (Q) {
      if (ne)
        for (me = I.call(T.ownerDocument); T.firstChild; )
          me.appendChild(T.firstChild);
      else
        me = T;
      return (V.shadowroot || V.shadowrootmode) && (me = z.call(n, me, !0)), me;
    }
    let ye = W ? T.outerHTML : T.innerHTML;
    return W && v["!doctype"] && T.ownerDocument && T.ownerDocument.doctype && T.ownerDocument.doctype.name && be(tr, T.ownerDocument.doctype.name) && (ye = "<!DOCTYPE " + T.ownerDocument.doctype.name + `>
` + ye), de && Mn([U, ie, J], (tt) => {
      ye = on(ye, tt, " ");
    }), p && Se ? p.createHTML(ye) : ye;
  }, e.setConfig = function() {
    let M = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    sl(M), G = !0;
  }, e.clearConfig = function() {
    Gt = null, G = !1;
  }, e.isValidAttribute = function(M, h, T) {
    Gt || sl({});
    const O = se(M), Y = se(h);
    return ki(O, Y, T);
  }, e.addHook = function(M, h) {
    typeof h == "function" && (C[M] = C[M] || [], ln(C[M], h));
  }, e.removeHook = function(M) {
    if (C[M])
      return qo(C[M]);
  }, e.removeHooks = function(M) {
    C[M] && (C[M] = []);
  }, e.removeAllHooks = function() {
    C = {};
  }, e;
}
nr();
const Yo = (l) => {
  let e = ["B", "KB", "MB", "GB", "PB"], t = 0;
  for (; l > 1024; )
    l /= 1024, t++;
  let n = e[t];
  return l.toFixed(1) + "&nbsp;" + n;
}, {
  HtmlTag: q_,
  SvelteComponent: B_,
  append: Re,
  attr: De,
  check_outros: lr,
  create_component: H_,
  destroy_component: j_,
  detach: gn,
  element: ot,
  ensure_array_like: Xo,
  group_outros: ir,
  init: W_,
  insert: pn,
  listen: Ql,
  mount_component: G_,
  noop: Zo,
  outro_and_destroy_block: V_,
  run_all: Y_,
  safe_not_equal: X_,
  set_data: xl,
  set_style: Ko,
  space: Pn,
  text: Kn,
  toggle_class: Jo,
  transition_in: Jn,
  transition_out: Qn,
  update_keyed_each: Z_
} = window.__gradio__svelte__internal, { createEventDispatcher: K_ } = window.__gradio__svelte__internal;
function Qo(l, e, t) {
  const n = l.slice();
  return n[11] = e[t], n[13] = t, n;
}
function J_(l) {
  let e = (
    /*i18n*/
    l[2]("file.uploading") + ""
  ), t;
  return {
    c() {
      t = Kn(e);
    },
    m(n, i) {
      pn(n, t, i);
    },
    p(n, i) {
      i & /*i18n*/
      4 && e !== (e = /*i18n*/
      n[2]("file.uploading") + "") && xl(t, e);
    },
    i: Zo,
    o: Zo,
    d(n) {
      n && gn(t);
    }
  };
}
function Q_(l) {
  let e, t;
  return e = new Fa({
    props: {
      href: (
        /*file*/
        l[11].url
      ),
      download: window.__is_colab__ ? null : (
        /*file*/
        l[11].orig_name
      ),
      $$slots: { default: [x_] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      H_(e.$$.fragment);
    },
    m(n, i) {
      G_(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*normalized_files*/
      8 && (o.href = /*file*/
      n[11].url), i & /*normalized_files*/
      8 && (o.download = window.__is_colab__ ? null : (
        /*file*/
        n[11].orig_name
      )), i & /*$$scope, normalized_files*/
      16392 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Jn(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Qn(e.$$.fragment, n), t = !1;
    },
    d(n) {
      j_(e, n);
    }
  };
}
function x_(l) {
  let e, t = (
    /*file*/
    (l[11].size != null ? Yo(
      /*file*/
      l[11].size
    ) : "(size unknown)") + ""
  ), n;
  return {
    c() {
      e = new q_(!1), n = Kn(" ⇣"), e.a = n;
    },
    m(i, o) {
      e.m(t, i, o), pn(i, n, o);
    },
    p(i, o) {
      o & /*normalized_files*/
      8 && t !== (t = /*file*/
      (i[11].size != null ? Yo(
        /*file*/
        i[11].size
      ) : "(size unknown)") + "") && e.p(t);
    },
    d(i) {
      i && (e.d(), gn(n));
    }
  };
}
function xo(l) {
  let e, t, n, i;
  function o() {
    return (
      /*click_handler*/
      l[7](
        /*i*/
        l[13]
      )
    );
  }
  function s(...f) {
    return (
      /*keydown_handler*/
      l[8](
        /*i*/
        l[13],
        ...f
      )
    );
  }
  return {
    c() {
      e = ot("td"), t = ot("button"), t.textContent = "×", De(t, "class", "label-clear-button svelte-1g4vug2"), De(t, "aria-label", "Remove this file"), De(e, "class", "svelte-1g4vug2");
    },
    m(f, r) {
      pn(f, e, r), Re(e, t), n || (i = [
        Ql(t, "click", o),
        Ql(t, "keydown", s)
      ], n = !0);
    },
    p(f, r) {
      l = f;
    },
    d(f) {
      f && gn(e), n = !1, Y_(i);
    }
  };
}
function $o(l, e) {
  let t, n, i, o = (
    /*file*/
    e[11].filename_stem + ""
  ), s, f, r, a = (
    /*file*/
    e[11].filename_ext + ""
  ), u, c, _, d, m, g, y, E, k, w, p;
  const R = [Q_, J_], b = [];
  function F(z, C) {
    return (
      /*file*/
      z[11].url ? 0 : 1
    );
  }
  m = F(e), g = b[m] = R[m](e);
  let I = (
    /*normalized_files*/
    e[3].length > 1 && xo(e)
  );
  function D(...z) {
    return (
      /*click_handler_1*/
      e[9](
        /*i*/
        e[13],
        ...z
      )
    );
  }
  return {
    key: l,
    first: null,
    c() {
      t = ot("tr"), n = ot("td"), i = ot("span"), s = Kn(o), f = Pn(), r = ot("span"), u = Kn(a), _ = Pn(), d = ot("td"), g.c(), y = Pn(), I && I.c(), E = Pn(), De(i, "class", "stem svelte-1g4vug2"), De(r, "class", "ext svelte-1g4vug2"), De(n, "class", "filename svelte-1g4vug2"), De(n, "aria-label", c = /*file*/
      e[11].orig_name), De(d, "class", "download svelte-1g4vug2"), De(t, "class", "file svelte-1g4vug2"), Jo(
        t,
        "selectable",
        /*selectable*/
        e[0]
      ), this.first = t;
    },
    m(z, C) {
      pn(z, t, C), Re(t, n), Re(n, i), Re(i, s), Re(n, f), Re(n, r), Re(r, u), Re(t, _), Re(t, d), b[m].m(d, null), Re(t, y), I && I.m(t, null), Re(t, E), k = !0, w || (p = Ql(t, "click", D), w = !0);
    },
    p(z, C) {
      e = z, (!k || C & /*normalized_files*/
      8) && o !== (o = /*file*/
      e[11].filename_stem + "") && xl(s, o), (!k || C & /*normalized_files*/
      8) && a !== (a = /*file*/
      e[11].filename_ext + "") && xl(u, a), (!k || C & /*normalized_files*/
      8 && c !== (c = /*file*/
      e[11].orig_name)) && De(n, "aria-label", c);
      let U = m;
      m = F(e), m === U ? b[m].p(e, C) : (ir(), Qn(b[U], 1, 1, () => {
        b[U] = null;
      }), lr(), g = b[m], g ? g.p(e, C) : (g = b[m] = R[m](e), g.c()), Jn(g, 1), g.m(d, null)), /*normalized_files*/
      e[3].length > 1 ? I ? I.p(e, C) : (I = xo(e), I.c(), I.m(t, E)) : I && (I.d(1), I = null), (!k || C & /*selectable*/
      1) && Jo(
        t,
        "selectable",
        /*selectable*/
        e[0]
      );
    },
    i(z) {
      k || (Jn(g), k = !0);
    },
    o(z) {
      Qn(g), k = !1;
    },
    d(z) {
      z && gn(t), b[m].d(), I && I.d(), w = !1, p();
    }
  };
}
function $_(l) {
  let e, t, n, i = [], o = /* @__PURE__ */ new Map(), s, f = Xo(
    /*normalized_files*/
    l[3]
  );
  const r = (a) => (
    /*file*/
    a[11]
  );
  for (let a = 0; a < f.length; a += 1) {
    let u = Qo(l, f, a), c = r(u);
    o.set(c, i[a] = $o(c, u));
  }
  return {
    c() {
      e = ot("div"), t = ot("table"), n = ot("tbody");
      for (let a = 0; a < i.length; a += 1)
        i[a].c();
      De(n, "class", "svelte-1g4vug2"), De(t, "class", "file-preview svelte-1g4vug2"), De(e, "class", "file-preview-holder svelte-1g4vug2"), Ko(e, "max-height", typeof /*height*/
      l[1] === void 0 ? "auto" : (
        /*height*/
        l[1] + "px"
      ));
    },
    m(a, u) {
      pn(a, e, u), Re(e, t), Re(t, n);
      for (let c = 0; c < i.length; c += 1)
        i[c] && i[c].m(n, null);
      s = !0;
    },
    p(a, [u]) {
      u & /*selectable, handle_row_click, normalized_files, remove_file, window, i18n*/
      61 && (f = Xo(
        /*normalized_files*/
        a[3]
      ), ir(), i = Z_(i, u, r, 1, a, f, o, n, V_, $o, null, Qo), lr()), (!s || u & /*height*/
      2) && Ko(e, "max-height", typeof /*height*/
      a[1] === void 0 ? "auto" : (
        /*height*/
        a[1] + "px"
      ));
    },
    i(a) {
      if (!s) {
        for (let u = 0; u < f.length; u += 1)
          Jn(i[u]);
        s = !0;
      }
    },
    o(a) {
      for (let u = 0; u < i.length; u += 1)
        Qn(i[u]);
      s = !1;
    },
    d(a) {
      a && gn(e);
      for (let u = 0; u < i.length; u += 1)
        i[u].d();
    }
  };
}
function ed(l) {
  const e = l.lastIndexOf(".");
  return e === -1 ? [l, ""] : [l.slice(0, e), l.slice(e)];
}
function td(l, e, t) {
  let n;
  const i = K_();
  let { value: o } = e, { selectable: s = !1 } = e, { height: f = void 0 } = e, { i18n: r } = e;
  function a(m, g) {
    const y = m.currentTarget;
    (m.target === y || // Only select if the click is on the row itself
    y && y.firstElementChild && m.composedPath().includes(y.firstElementChild)) && i("select", {
      value: n[g].orig_name,
      index: g
    });
  }
  function u(m) {
    const g = n.splice(m, 1);
    t(3, n = [...n]), t(6, o = n), i("delete", g[0]), i("change", n);
  }
  const c = (m) => {
    u(m);
  }, _ = (m, g) => {
    g.key === "Enter" && u(m);
  }, d = (m, g) => {
    a(g, m);
  };
  return l.$$set = (m) => {
    "value" in m && t(6, o = m.value), "selectable" in m && t(0, s = m.selectable), "height" in m && t(1, f = m.height), "i18n" in m && t(2, r = m.i18n);
  }, l.$$.update = () => {
    l.$$.dirty & /*value*/
    64 && t(3, n = (Array.isArray(o) ? o : [o]).map((m) => {
      var g;
      const [y, E] = ed((g = m.orig_name) !== null && g !== void 0 ? g : "");
      return Object.assign(Object.assign({}, m), { filename_stem: y, filename_ext: E });
    }));
  }, [
    s,
    f,
    r,
    n,
    a,
    u,
    o,
    c,
    _,
    d
  ];
}
class nd extends B_ {
  constructor(e) {
    super(), W_(this, e, td, $_, X_, {
      value: 6,
      selectable: 0,
      height: 1,
      i18n: 2
    });
  }
}
const {
  SvelteComponent: ld,
  add_flush_callback: id,
  bind: od,
  binding_callbacks: ad,
  bubble: Fn,
  check_outros: rd,
  create_component: xn,
  create_slot: sd,
  destroy_component: $n,
  detach: $l,
  empty: fd,
  get_all_dirty_from_scope: ud,
  get_slot_changes: cd,
  group_outros: _d,
  init: dd,
  insert: ei,
  mount_component: el,
  safe_not_equal: md,
  space: or,
  transition_in: Mt,
  transition_out: Nt,
  update_slot_base: hd
} = window.__gradio__svelte__internal, { createEventDispatcher: gd, tick: pd } = window.__gradio__svelte__internal;
function bd(l) {
  let e, t, n;
  function i(s) {
    l[19](s);
  }
  let o = {
    filetype: (
      /*file_types*/
      l[4]
    ),
    file_count: (
      /*file_count*/
      l[3]
    ),
    max_file_size: (
      /*max_file_size*/
      l[9]
    ),
    root: (
      /*root*/
      l[6]
    ),
    stream_handler: (
      /*stream_handler*/
      l[11]
    ),
    upload: (
      /*upload*/
      l[10]
    ),
    $$slots: { default: [vd] },
    $$scope: { ctx: l }
  };
  return (
    /*dragging*/
    l[12] !== void 0 && (o.dragging = /*dragging*/
    l[12]), e = new Pu({ props: o }), ad.push(() => od(e, "dragging", i)), e.$on(
      "load",
      /*handle_upload*/
      l[13]
    ), e.$on(
      "error",
      /*error_handler*/
      l[20]
    ), {
      c() {
        xn(e.$$.fragment);
      },
      m(s, f) {
        el(e, s, f), n = !0;
      },
      p(s, f) {
        const r = {};
        f & /*file_types*/
        16 && (r.filetype = /*file_types*/
        s[4]), f & /*file_count*/
        8 && (r.file_count = /*file_count*/
        s[3]), f & /*max_file_size*/
        512 && (r.max_file_size = /*max_file_size*/
        s[9]), f & /*root*/
        64 && (r.root = /*root*/
        s[6]), f & /*stream_handler*/
        2048 && (r.stream_handler = /*stream_handler*/
        s[11]), f & /*upload*/
        1024 && (r.upload = /*upload*/
        s[10]), f & /*$$scope*/
        2097152 && (r.$$scope = { dirty: f, ctx: s }), !t && f & /*dragging*/
        4096 && (t = !0, r.dragging = /*dragging*/
        s[12], id(() => t = !1)), e.$set(r);
      },
      i(s) {
        n || (Mt(e.$$.fragment, s), n = !0);
      },
      o(s) {
        Nt(e.$$.fragment, s), n = !1;
      },
      d(s) {
        $n(e, s);
      }
    }
  );
}
function wd(l) {
  let e, t, n, i;
  return e = new oi({
    props: { i18n: (
      /*i18n*/
      l[8]
    ), absolute: !0 }
  }), e.$on(
    "clear",
    /*handle_clear*/
    l[14]
  ), n = new nd({
    props: {
      i18n: (
        /*i18n*/
        l[8]
      ),
      selectable: (
        /*selectable*/
        l[5]
      ),
      value: (
        /*value*/
        l[0]
      ),
      height: (
        /*height*/
        l[7]
      )
    }
  }), n.$on(
    "select",
    /*select_handler*/
    l[16]
  ), n.$on(
    "change",
    /*change_handler*/
    l[17]
  ), n.$on(
    "delete",
    /*delete_handler*/
    l[18]
  ), {
    c() {
      xn(e.$$.fragment), t = or(), xn(n.$$.fragment);
    },
    m(o, s) {
      el(e, o, s), ei(o, t, s), el(n, o, s), i = !0;
    },
    p(o, s) {
      const f = {};
      s & /*i18n*/
      256 && (f.i18n = /*i18n*/
      o[8]), e.$set(f);
      const r = {};
      s & /*i18n*/
      256 && (r.i18n = /*i18n*/
      o[8]), s & /*selectable*/
      32 && (r.selectable = /*selectable*/
      o[5]), s & /*value*/
      1 && (r.value = /*value*/
      o[0]), s & /*height*/
      128 && (r.height = /*height*/
      o[7]), n.$set(r);
    },
    i(o) {
      i || (Mt(e.$$.fragment, o), Mt(n.$$.fragment, o), i = !0);
    },
    o(o) {
      Nt(e.$$.fragment, o), Nt(n.$$.fragment, o), i = !1;
    },
    d(o) {
      o && $l(t), $n(e, o), $n(n, o);
    }
  };
}
function vd(l) {
  let e;
  const t = (
    /*#slots*/
    l[15].default
  ), n = sd(
    t,
    l,
    /*$$scope*/
    l[21],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      2097152) && hd(
        n,
        t,
        i,
        /*$$scope*/
        i[21],
        e ? cd(
          t,
          /*$$scope*/
          i[21],
          o,
          null
        ) : ud(
          /*$$scope*/
          i[21]
        ),
        null
      );
    },
    i(i) {
      e || (Mt(n, i), e = !0);
    },
    o(i) {
      Nt(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function kd(l) {
  let e, t, n, i, o, s, f;
  e = new ra({
    props: {
      show_label: (
        /*show_label*/
        l[2]
      ),
      Icon: nf,
      float: !/*value*/
      l[0],
      label: (
        /*label*/
        l[1] || "File"
      )
    }
  });
  const r = [wd, bd], a = [];
  function u(c, _) {
    return _ & /*value*/
    1 && (n = null), n == null && (n = !!/*value*/
    (c[0] && (!Array.isArray(
      /*value*/
      c[0]
    ) || /*value*/
    c[0].length > 0))), n ? 0 : 1;
  }
  return i = u(l, -1), o = a[i] = r[i](l), {
    c() {
      xn(e.$$.fragment), t = or(), o.c(), s = fd();
    },
    m(c, _) {
      el(e, c, _), ei(c, t, _), a[i].m(c, _), ei(c, s, _), f = !0;
    },
    p(c, [_]) {
      const d = {};
      _ & /*show_label*/
      4 && (d.show_label = /*show_label*/
      c[2]), _ & /*value*/
      1 && (d.float = !/*value*/
      c[0]), _ & /*label*/
      2 && (d.label = /*label*/
      c[1] || "File"), e.$set(d);
      let m = i;
      i = u(c, _), i === m ? a[i].p(c, _) : (_d(), Nt(a[m], 1, 1, () => {
        a[m] = null;
      }), rd(), o = a[i], o ? o.p(c, _) : (o = a[i] = r[i](c), o.c()), Mt(o, 1), o.m(s.parentNode, s));
    },
    i(c) {
      f || (Mt(e.$$.fragment, c), Mt(o), f = !0);
    },
    o(c) {
      Nt(e.$$.fragment, c), Nt(o), f = !1;
    },
    d(c) {
      c && ($l(t), $l(s)), $n(e, c), a[i].d(c);
    }
  };
}
function yd(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(C, U, ie, J) {
    function ce(Z) {
      return Z instanceof ie ? Z : new ie(function(te) {
        te(Z);
      });
    }
    return new (ie || (ie = Promise))(function(Z, te) {
      function oe(v) {
        try {
          _e(J.next(v));
        } catch (ke) {
          te(ke);
        }
      }
      function Me(v) {
        try {
          _e(J.throw(v));
        } catch (ke) {
          te(ke);
        }
      }
      function _e(v) {
        v.done ? Z(v.value) : ce(v.value).then(oe, Me);
      }
      _e((J = J.apply(C, U || [])).next());
    });
  };
  let { value: s } = e, { label: f } = e, { show_label: r = !0 } = e, { file_count: a = "single" } = e, { file_types: u = null } = e, { selectable: c = !1 } = e, { root: _ } = e, { height: d = void 0 } = e, { i18n: m } = e, { max_file_size: g = null } = e, { upload: y } = e, { stream_handler: E } = e;
  function k(C) {
    return o(this, arguments, void 0, function* ({ detail: U }) {
      t(0, s = U), yield pd(), p("change", s), p("upload", U);
    });
  }
  function w() {
    t(0, s = null), p("change", null), p("clear");
  }
  const p = gd();
  let R = !1;
  function b(C) {
    Fn.call(this, l, C);
  }
  function F(C) {
    Fn.call(this, l, C);
  }
  function I(C) {
    Fn.call(this, l, C);
  }
  function D(C) {
    R = C, t(12, R);
  }
  function z(C) {
    Fn.call(this, l, C);
  }
  return l.$$set = (C) => {
    "value" in C && t(0, s = C.value), "label" in C && t(1, f = C.label), "show_label" in C && t(2, r = C.show_label), "file_count" in C && t(3, a = C.file_count), "file_types" in C && t(4, u = C.file_types), "selectable" in C && t(5, c = C.selectable), "root" in C && t(6, _ = C.root), "height" in C && t(7, d = C.height), "i18n" in C && t(8, m = C.i18n), "max_file_size" in C && t(9, g = C.max_file_size), "upload" in C && t(10, y = C.upload), "stream_handler" in C && t(11, E = C.stream_handler), "$$scope" in C && t(21, i = C.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*dragging*/
    4096 && p("drag", R);
  }, [
    s,
    f,
    r,
    a,
    u,
    c,
    _,
    d,
    m,
    g,
    y,
    E,
    R,
    k,
    w,
    n,
    b,
    F,
    I,
    D,
    z,
    i
  ];
}
class Ed extends ld {
  constructor(e) {
    super(), dd(this, e, yd, kd, md, {
      value: 0,
      label: 1,
      show_label: 2,
      file_count: 3,
      file_types: 4,
      selectable: 5,
      root: 6,
      height: 7,
      i18n: 8,
      max_file_size: 9,
      upload: 10,
      stream_handler: 11
    });
  }
}
const {
  SvelteComponent: Td,
  add_flush_callback: ea,
  assign: Ad,
  bind: ta,
  binding_callbacks: na,
  check_outros: Sd,
  create_component: bn,
  destroy_component: wn,
  detach: la,
  empty: Cd,
  get_spread_object: Ld,
  get_spread_update: Rd,
  group_outros: Dd,
  init: Od,
  insert: ia,
  mount_component: vn,
  safe_not_equal: Id,
  space: Md,
  transition_in: Pt,
  transition_out: Ft
} = window.__gradio__svelte__internal, { createEventDispatcher: Nd } = window.__gradio__svelte__internal;
function Pd(l) {
  let e, t, n, i;
  function o(r) {
    l[26](r);
  }
  function s(r) {
    l[27](r);
  }
  let f = {
    label: (
      /*label*/
      l[4]
    ),
    show_label: (
      /*show_label*/
      l[3]
    ),
    columns: (
      /*columns*/
      l[12]
    ),
    rows: (
      /*rows*/
      l[13]
    ),
    height: (
      /*height*/
      l[14]
    ),
    preview: (
      /*preview*/
      l[15]
    ),
    object_fit: (
      /*object_fit*/
      l[17]
    ),
    interactive: (
      /*interactive*/
      l[19]
    ),
    allow_preview: (
      /*allow_preview*/
      l[16]
    ),
    show_share_button: (
      /*show_share_button*/
      l[18]
    ),
    show_download_button: (
      /*show_download_button*/
      l[20]
    ),
    i18n: (
      /*gradio*/
      l[21].i18n
    ),
    _fetch: (
      /*gradio*/
      l[21].client.fetch
    )
  };
  return (
    /*selected_index*/
    l[1] !== void 0 && (f.selected_index = /*selected_index*/
    l[1]), /*value*/
    l[0] !== void 0 && (f.value = /*value*/
    l[0]), e = new zc({ props: f }), na.push(() => ta(e, "selected_index", o)), na.push(() => ta(e, "value", s)), e.$on(
      "change",
      /*change_handler*/
      l[28]
    ), e.$on(
      "select",
      /*select_handler*/
      l[29]
    ), e.$on(
      "unselect",
      /*unselect_handler*/
      l[30]
    ), e.$on(
      "share",
      /*share_handler*/
      l[31]
    ), e.$on(
      "error",
      /*error_handler_1*/
      l[32]
    ), {
      c() {
        bn(e.$$.fragment);
      },
      m(r, a) {
        vn(e, r, a), i = !0;
      },
      p(r, a) {
        const u = {};
        a[0] & /*label*/
        16 && (u.label = /*label*/
        r[4]), a[0] & /*show_label*/
        8 && (u.show_label = /*show_label*/
        r[3]), a[0] & /*columns*/
        4096 && (u.columns = /*columns*/
        r[12]), a[0] & /*rows*/
        8192 && (u.rows = /*rows*/
        r[13]), a[0] & /*height*/
        16384 && (u.height = /*height*/
        r[14]), a[0] & /*preview*/
        32768 && (u.preview = /*preview*/
        r[15]), a[0] & /*object_fit*/
        131072 && (u.object_fit = /*object_fit*/
        r[17]), a[0] & /*interactive*/
        524288 && (u.interactive = /*interactive*/
        r[19]), a[0] & /*allow_preview*/
        65536 && (u.allow_preview = /*allow_preview*/
        r[16]), a[0] & /*show_share_button*/
        262144 && (u.show_share_button = /*show_share_button*/
        r[18]), a[0] & /*show_download_button*/
        1048576 && (u.show_download_button = /*show_download_button*/
        r[20]), a[0] & /*gradio*/
        2097152 && (u.i18n = /*gradio*/
        r[21].i18n), a[0] & /*gradio*/
        2097152 && (u._fetch = /*gradio*/
        r[21].client.fetch), !t && a[0] & /*selected_index*/
        2 && (t = !0, u.selected_index = /*selected_index*/
        r[1], ea(() => t = !1)), !n && a[0] & /*value*/
        1 && (n = !0, u.value = /*value*/
        r[0], ea(() => n = !1)), e.$set(u);
      },
      i(r) {
        i || (Pt(e.$$.fragment, r), i = !0);
      },
      o(r) {
        Ft(e.$$.fragment, r), i = !1;
      },
      d(r) {
        wn(e, r);
      }
    }
  );
}
function Fd(l) {
  let e, t;
  return e = new Ed({
    props: {
      value: null,
      root: (
        /*root*/
        l[5]
      ),
      label: (
        /*label*/
        l[4]
      ),
      max_file_size: (
        /*gradio*/
        l[21].max_file_size
      ),
      file_count: "multiple",
      file_types: ["image"],
      i18n: (
        /*gradio*/
        l[21].i18n
      ),
      upload: (
        /*gradio*/
        l[21].client.upload
      ),
      stream_handler: (
        /*gradio*/
        l[21].client.stream
      ),
      $$slots: { default: [zd] },
      $$scope: { ctx: l }
    }
  }), e.$on(
    "upload",
    /*upload_handler*/
    l[24]
  ), e.$on(
    "error",
    /*error_handler*/
    l[25]
  ), {
    c() {
      bn(e.$$.fragment);
    },
    m(n, i) {
      vn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*root*/
      32 && (o.root = /*root*/
      n[5]), i[0] & /*label*/
      16 && (o.label = /*label*/
      n[4]), i[0] & /*gradio*/
      2097152 && (o.max_file_size = /*gradio*/
      n[21].max_file_size), i[0] & /*gradio*/
      2097152 && (o.i18n = /*gradio*/
      n[21].i18n), i[0] & /*gradio*/
      2097152 && (o.upload = /*gradio*/
      n[21].client.upload), i[0] & /*gradio*/
      2097152 && (o.stream_handler = /*gradio*/
      n[21].client.stream), i[0] & /*gradio*/
      2097152 | i[1] & /*$$scope*/
      8 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Pt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ft(e.$$.fragment, n), t = !1;
    },
    d(n) {
      wn(e, n);
    }
  };
}
function zd(l) {
  let e, t;
  return e = new tu({
    props: {
      i18n: (
        /*gradio*/
        l[21].i18n
      ),
      type: "gallery"
    }
  }), {
    c() {
      bn(e.$$.fragment);
    },
    m(n, i) {
      vn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*gradio*/
      2097152 && (o.i18n = /*gradio*/
      n[21].i18n), e.$set(o);
    },
    i(n) {
      t || (Pt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ft(e.$$.fragment, n), t = !1;
    },
    d(n) {
      wn(e, n);
    }
  };
}
function Ud(l) {
  let e, t, n, i, o, s;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        l[21].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[21].i18n
    ) },
    /*loading_status*/
    l[2]
  ];
  let r = {};
  for (let _ = 0; _ < f.length; _ += 1)
    r = Ad(r, f[_]);
  e = new w_({ props: r }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[23]
  );
  const a = [Fd, Pd], u = [];
  function c(_, d) {
    return (
      /*interactive*/
      _[19] && /*no_value*/
      _[22] ? 0 : 1
    );
  }
  return n = c(l), i = u[n] = a[n](l), {
    c() {
      bn(e.$$.fragment), t = Md(), i.c(), o = Cd();
    },
    m(_, d) {
      vn(e, _, d), ia(_, t, d), u[n].m(_, d), ia(_, o, d), s = !0;
    },
    p(_, d) {
      const m = d[0] & /*gradio, loading_status*/
      2097156 ? Rd(f, [
        d[0] & /*gradio*/
        2097152 && {
          autoscroll: (
            /*gradio*/
            _[21].autoscroll
          )
        },
        d[0] & /*gradio*/
        2097152 && { i18n: (
          /*gradio*/
          _[21].i18n
        ) },
        d[0] & /*loading_status*/
        4 && Ld(
          /*loading_status*/
          _[2]
        )
      ]) : {};
      e.$set(m);
      let g = n;
      n = c(_), n === g ? u[n].p(_, d) : (Dd(), Ft(u[g], 1, 1, () => {
        u[g] = null;
      }), Sd(), i = u[n], i ? i.p(_, d) : (i = u[n] = a[n](_), i.c()), Pt(i, 1), i.m(o.parentNode, o));
    },
    i(_) {
      s || (Pt(e.$$.fragment, _), Pt(i), s = !0);
    },
    o(_) {
      Ft(e.$$.fragment, _), Ft(i), s = !1;
    },
    d(_) {
      _ && (la(t), la(o)), wn(e, _), u[n].d(_);
    }
  };
}
function qd(l) {
  let e, t;
  return e = new Lr({
    props: {
      visible: (
        /*visible*/
        l[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[6]
      ),
      elem_classes: (
        /*elem_classes*/
        l[7]
      ),
      container: (
        /*container*/
        l[9]
      ),
      scale: (
        /*scale*/
        l[10]
      ),
      min_width: (
        /*min_width*/
        l[11]
      ),
      allow_overflow: !1,
      height: typeof /*height*/
      l[14] == "number" ? (
        /*height*/
        l[14]
      ) : void 0,
      $$slots: { default: [Ud] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      bn(e.$$.fragment);
    },
    m(n, i) {
      vn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      n[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      n[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      n[7]), i[0] & /*container*/
      512 && (o.container = /*container*/
      n[9]), i[0] & /*scale*/
      1024 && (o.scale = /*scale*/
      n[10]), i[0] & /*min_width*/
      2048 && (o.min_width = /*min_width*/
      n[11]), i[0] & /*height*/
      16384 && (o.height = typeof /*height*/
      n[14] == "number" ? (
        /*height*/
        n[14]
      ) : void 0), i[0] & /*root, label, gradio, value, loading_status, interactive, no_value, show_label, columns, rows, height, preview, object_fit, allow_preview, show_share_button, show_download_button, selected_index*/
      8384575 | i[1] & /*$$scope*/
      8 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Pt(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ft(e.$$.fragment, n), t = !1;
    },
    d(n) {
      wn(e, n);
    }
  };
}
function Bd(l, e, t) {
  let n, { loading_status: i } = e, { show_label: o } = e, { label: s } = e, { root: f } = e, { elem_id: r = "" } = e, { elem_classes: a = [] } = e, { visible: u = !0 } = e, { value: c = null } = e, { container: _ = !0 } = e, { scale: d = null } = e, { min_width: m = void 0 } = e, { columns: g = [2] } = e, { rows: y = void 0 } = e, { height: E = "auto" } = e, { preview: k } = e, { allow_preview: w = !0 } = e, { selected_index: p = null } = e, { object_fit: R = "cover" } = e, { show_share_button: b = !1 } = e, { interactive: F } = e, { show_download_button: I = !1 } = e, { gradio: D } = e;
  const z = Nd(), C = () => D.dispatch("clear_status", i), U = (v) => {
    const ke = Array.isArray(v.detail) ? v.detail : [v.detail];
    t(0, c = ke.map((V) => ({ image: V, caption: null }))), D.dispatch("upload", c);
  }, ie = ({ detail: v }) => {
    t(2, i = i || {}), t(2, i.status = "error", i), D.dispatch("error", v);
  };
  function J(v) {
    p = v, t(1, p);
  }
  function ce(v) {
    c = v, t(0, c);
  }
  const Z = () => D.dispatch("change", c), te = (v) => D.dispatch("select", v.detail), oe = (v) => D.dispatch("unselect", v.detail), Me = (v) => D.dispatch("share", v.detail), _e = (v) => D.dispatch("error", v.detail);
  return l.$$set = (v) => {
    "loading_status" in v && t(2, i = v.loading_status), "show_label" in v && t(3, o = v.show_label), "label" in v && t(4, s = v.label), "root" in v && t(5, f = v.root), "elem_id" in v && t(6, r = v.elem_id), "elem_classes" in v && t(7, a = v.elem_classes), "visible" in v && t(8, u = v.visible), "value" in v && t(0, c = v.value), "container" in v && t(9, _ = v.container), "scale" in v && t(10, d = v.scale), "min_width" in v && t(11, m = v.min_width), "columns" in v && t(12, g = v.columns), "rows" in v && t(13, y = v.rows), "height" in v && t(14, E = v.height), "preview" in v && t(15, k = v.preview), "allow_preview" in v && t(16, w = v.allow_preview), "selected_index" in v && t(1, p = v.selected_index), "object_fit" in v && t(17, R = v.object_fit), "show_share_button" in v && t(18, b = v.show_share_button), "interactive" in v && t(19, F = v.interactive), "show_download_button" in v && t(20, I = v.show_download_button), "gradio" in v && t(21, D = v.gradio);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1 && t(22, n = Array.isArray(c) ? c.length === 0 : !c), l.$$.dirty[0] & /*selected_index*/
    2 && z("prop_change", { selected_index: p });
  }, [
    c,
    p,
    i,
    o,
    s,
    f,
    r,
    a,
    u,
    _,
    d,
    m,
    g,
    y,
    E,
    k,
    w,
    R,
    b,
    F,
    I,
    D,
    n,
    C,
    U,
    ie,
    J,
    ce,
    Z,
    te,
    oe,
    Me,
    _e
  ];
}
class Yd extends Td {
  constructor(e) {
    super(), Od(
      this,
      e,
      Bd,
      qd,
      Id,
      {
        loading_status: 2,
        show_label: 3,
        label: 4,
        root: 5,
        elem_id: 6,
        elem_classes: 7,
        visible: 8,
        value: 0,
        container: 9,
        scale: 10,
        min_width: 11,
        columns: 12,
        rows: 13,
        height: 14,
        preview: 15,
        allow_preview: 16,
        selected_index: 1,
        object_fit: 17,
        show_share_button: 18,
        interactive: 19,
        show_download_button: 20,
        gradio: 21
      },
      null,
      [-1, -1]
    );
  }
}
export {
  zc as BaseGallery,
  Yd as default
};
