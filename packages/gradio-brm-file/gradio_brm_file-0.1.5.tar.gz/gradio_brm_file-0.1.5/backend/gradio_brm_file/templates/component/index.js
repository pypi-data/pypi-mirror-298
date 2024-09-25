const {
  SvelteComponent: Zt,
  assign: jt,
  create_slot: Bt,
  detach: Et,
  element: Dt,
  get_all_dirty_from_scope: Pt,
  get_slot_changes: Wt,
  get_spread_update: Rt,
  init: Tt,
  insert: Ut,
  safe_not_equal: Xt,
  set_dynamic_element_data: Pe,
  set_style: E,
  toggle_class: J,
  transition_in: mt,
  transition_out: ht,
  update_slot_base: Yt
} = window.__gradio__svelte__internal;
function Gt(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), f = Bt(
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
  ], r = {};
  for (let o = 0; o < s.length; o += 1)
    r = jt(r, s[o]);
  return {
    c() {
      e = Dt(
        /*tag*/
        l[14]
      ), f && f.c(), Pe(
        /*tag*/
        l[14]
      )(e, r), J(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), J(
        e,
        "padded",
        /*padding*/
        l[6]
      ), J(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), J(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), J(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), E(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), E(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), E(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), E(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), E(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), E(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), E(e, "border-width", "var(--block-border-width)");
    },
    m(o, a) {
      Ut(o, e, a), f && f.m(e, null), n = !0;
    },
    p(o, a) {
      f && f.p && (!n || a & /*$$scope*/
      131072) && Yt(
        f,
        i,
        o,
        /*$$scope*/
        o[17],
        n ? Wt(
          i,
          /*$$scope*/
          o[17],
          a,
          null
        ) : Pt(
          /*$$scope*/
          o[17]
        ),
        null
      ), Pe(
        /*tag*/
        o[14]
      )(e, r = Rt(s, [
        (!n || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!n || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!n || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), J(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), J(
        e,
        "padded",
        /*padding*/
        o[6]
      ), J(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), J(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), J(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), a & /*height*/
      1 && E(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), a & /*width*/
      2 && E(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), a & /*variant*/
      16 && E(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), a & /*allow_overflow*/
      2048 && E(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && E(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), a & /*min_width*/
      8192 && E(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      n || (mt(f, o), n = !0);
    },
    o(o) {
      ht(f, o), n = !1;
    },
    d(o) {
      o && Et(e), f && f.d(o);
    }
  };
}
function Ot(l) {
  let e, t = (
    /*tag*/
    l[14] && Gt(l)
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
      e || (mt(t, n), e = !0);
    },
    o(n) {
      ht(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Ht(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { variant: a = "solid" } = e, { border_mode: c = "base" } = e, { padding: u = !0 } = e, { type: p = "normal" } = e, { test_id: h = void 0 } = e, { explicit_call: y = !1 } = e, { container: F = !0 } = e, { visible: q = !0 } = e, { allow_overflow: L = !0 } = e, { scale: d = null } = e, { min_width: _ = 0 } = e, v = p === "fieldset" ? "fieldset" : "div";
  const V = (b) => {
    if (b !== void 0) {
      if (typeof b == "number")
        return b + "px";
      if (typeof b == "string")
        return b;
    }
  };
  return l.$$set = (b) => {
    "height" in b && t(0, f = b.height), "width" in b && t(1, s = b.width), "elem_id" in b && t(2, r = b.elem_id), "elem_classes" in b && t(3, o = b.elem_classes), "variant" in b && t(4, a = b.variant), "border_mode" in b && t(5, c = b.border_mode), "padding" in b && t(6, u = b.padding), "type" in b && t(16, p = b.type), "test_id" in b && t(7, h = b.test_id), "explicit_call" in b && t(8, y = b.explicit_call), "container" in b && t(9, F = b.container), "visible" in b && t(10, q = b.visible), "allow_overflow" in b && t(11, L = b.allow_overflow), "scale" in b && t(12, d = b.scale), "min_width" in b && t(13, _ = b.min_width), "$$scope" in b && t(17, i = b.$$scope);
  }, [
    f,
    s,
    r,
    o,
    a,
    c,
    u,
    h,
    y,
    F,
    q,
    L,
    d,
    _,
    v,
    V,
    p,
    i,
    n
  ];
}
class Jt extends Zt {
  constructor(e) {
    super(), Tt(this, e, Ht, Ot, Xt, {
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
  SvelteComponent: Qt,
  append: Ie,
  attr: ne,
  bubble: xt,
  create_component: $t,
  destroy_component: el,
  detach: bt,
  element: Ze,
  init: tl,
  insert: gt,
  listen: ll,
  mount_component: nl,
  safe_not_equal: il,
  set_data: fl,
  set_style: _e,
  space: sl,
  text: ol,
  toggle_class: I,
  transition_in: al,
  transition_out: rl
} = window.__gradio__svelte__internal;
function We(l) {
  let e, t;
  return {
    c() {
      e = Ze("span"), t = ol(
        /*label*/
        l[1]
      ), ne(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      gt(n, e, i), Ie(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && fl(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && bt(e);
    }
  };
}
function cl(l) {
  let e, t, n, i, f, s, r, o = (
    /*show_label*/
    l[2] && We(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = Ze("button"), o && o.c(), t = sl(), n = Ze("div"), $t(i.$$.fragment), ne(n, "class", "svelte-1lrphxw"), I(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), I(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), I(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], ne(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), ne(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), ne(
        e,
        "title",
        /*label*/
        l[1]
      ), ne(e, "class", "svelte-1lrphxw"), I(
        e,
        "pending",
        /*pending*/
        l[3]
      ), I(
        e,
        "padded",
        /*padded*/
        l[5]
      ), I(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), I(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), _e(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), _e(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), _e(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(a, c) {
      gt(a, e, c), o && o.m(e, null), Ie(e, t), Ie(e, n), nl(i, n, null), f = !0, s || (r = ll(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(a, [c]) {
      /*show_label*/
      a[2] ? o ? o.p(a, c) : (o = We(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), (!f || c & /*size*/
      16) && I(
        n,
        "small",
        /*size*/
        a[4] === "small"
      ), (!f || c & /*size*/
      16) && I(
        n,
        "large",
        /*size*/
        a[4] === "large"
      ), (!f || c & /*size*/
      16) && I(
        n,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!f || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!f || c & /*label*/
      2) && ne(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || c & /*hasPopup*/
      256) && ne(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || c & /*label*/
      2) && ne(
        e,
        "title",
        /*label*/
        a[1]
      ), (!f || c & /*pending*/
      8) && I(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!f || c & /*padded*/
      32) && I(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!f || c & /*highlight*/
      64) && I(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!f || c & /*transparent*/
      512) && I(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), c & /*disabled, _color*/
      4224 && _e(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && _e(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), c & /*offset*/
      2048 && _e(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (al(i.$$.fragment, a), f = !0);
    },
    o(a) {
      rl(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && bt(e), o && o.d(), el(i), s = !1, r();
    }
  };
}
function ul(l, e, t) {
  let n, { Icon: i } = e, { label: f = "" } = e, { show_label: s = !1 } = e, { pending: r = !1 } = e, { size: o = "small" } = e, { padded: a = !0 } = e, { highlight: c = !1 } = e, { disabled: u = !1 } = e, { hasPopup: p = !1 } = e, { color: h = "var(--block-label-text-color)" } = e, { transparent: y = !1 } = e, { background: F = "var(--background-fill-primary)" } = e, { offset: q = 0 } = e;
  function L(d) {
    xt.call(this, l, d);
  }
  return l.$$set = (d) => {
    "Icon" in d && t(0, i = d.Icon), "label" in d && t(1, f = d.label), "show_label" in d && t(2, s = d.show_label), "pending" in d && t(3, r = d.pending), "size" in d && t(4, o = d.size), "padded" in d && t(5, a = d.padded), "highlight" in d && t(6, c = d.highlight), "disabled" in d && t(7, u = d.disabled), "hasPopup" in d && t(8, p = d.hasPopup), "color" in d && t(13, h = d.color), "transparent" in d && t(9, y = d.transparent), "background" in d && t(10, F = d.background), "offset" in d && t(11, q = d.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = c ? "var(--color-accent)" : h);
  }, [
    i,
    f,
    s,
    r,
    o,
    a,
    c,
    u,
    p,
    y,
    F,
    q,
    n,
    h,
    L
  ];
}
class _l extends Qt {
  constructor(e) {
    super(), tl(this, e, ul, cl, il, {
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
  SvelteComponent: dl,
  append: Ve,
  attr: T,
  detach: ml,
  init: hl,
  insert: bl,
  noop: Ke,
  safe_not_equal: gl,
  set_style: Q,
  svg_element: ye
} = window.__gradio__svelte__internal;
function wl(l) {
  let e, t, n, i;
  return {
    c() {
      e = ye("svg"), t = ye("g"), n = ye("path"), i = ye("path"), T(n, "d", "M18,6L6.087,17.913"), Q(n, "fill", "none"), Q(n, "fill-rule", "nonzero"), Q(n, "stroke-width", "2px"), T(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), T(i, "d", "M4.364,4.364L19.636,19.636"), Q(i, "fill", "none"), Q(i, "fill-rule", "nonzero"), Q(i, "stroke-width", "2px"), T(e, "width", "100%"), T(e, "height", "100%"), T(e, "viewBox", "0 0 24 24"), T(e, "version", "1.1"), T(e, "xmlns", "http://www.w3.org/2000/svg"), T(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), T(e, "xml:space", "preserve"), T(e, "stroke", "currentColor"), Q(e, "fill-rule", "evenodd"), Q(e, "clip-rule", "evenodd"), Q(e, "stroke-linecap", "round"), Q(e, "stroke-linejoin", "round");
    },
    m(f, s) {
      bl(f, e, s), Ve(e, t), Ve(t, n), Ve(e, i);
    },
    p: Ke,
    i: Ke,
    o: Ke,
    d(f) {
      f && ml(e);
    }
  };
}
class kl extends dl {
  constructor(e) {
    super(), hl(this, e, null, wl, gl, {});
  }
}
const pl = [
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
], Re = {
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
pl.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Re[e][t],
      secondary: Re[e][n]
    }
  }),
  {}
);
function me(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ce() {
}
function yl(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const wt = typeof window < "u";
let Te = wt ? () => window.performance.now() : () => Date.now(), kt = wt ? (l) => requestAnimationFrame(l) : Ce;
const he = /* @__PURE__ */ new Set();
function pt(l) {
  he.forEach((e) => {
    e.c(l) || (he.delete(e), e.f());
  }), he.size !== 0 && kt(pt);
}
function vl(l) {
  let e;
  return he.size === 0 && kt(pt), {
    promise: new Promise((t) => {
      he.add(e = { c: l, f: t });
    }),
    abort() {
      he.delete(e);
    }
  };
}
const de = [];
function ql(l, e = Ce) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (yl(l, r) && (l = r, t)) {
      const o = !de.length;
      for (const a of n)
        a[1](), de.push(a, l);
      if (o) {
        for (let a = 0; a < de.length; a += 2)
          de[a][0](de[a + 1]);
        de.length = 0;
      }
    }
  }
  function f(r) {
    i(r(l));
  }
  function s(r, o = Ce) {
    const a = [r, o];
    return n.add(a), n.size === 1 && (t = e(i, f) || Ce), r(l), () => {
      n.delete(a), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function Ue(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function je(l, e, t, n) {
  if (typeof t == "number" || Ue(t)) {
    const i = n - t, f = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, r = l.opts.damping * f, o = (s - r) * l.inv_mass, a = (f + o) * l.dt;
    return Math.abs(a) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Ue(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => je(l, e[f], t[f], n[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = je(l, e[f], t[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Xe(l, e = {}) {
  const t = ql(l), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, r, o, a = l, c = l, u = 1, p = 0, h = !1;
  function y(q, L = {}) {
    c = q;
    const d = o = {};
    return l == null || L.hard || F.stiffness >= 1 && F.damping >= 1 ? (h = !0, s = Te(), a = q, t.set(l = c), Promise.resolve()) : (L.soft && (p = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), u = 0), r || (s = Te(), h = !1, r = vl((_) => {
      if (h)
        return h = !1, r = null, !1;
      u = Math.min(u + p, 1);
      const v = {
        inv_mass: u,
        opts: F,
        settled: !0,
        dt: (_ - s) * 60 / 1e3
      }, V = je(v, a, l, c);
      return s = _, a = l, t.set(l = V), v.settled && (r = null), !v.settled;
    })), new Promise((_) => {
      r.promise.then(() => {
        d === o && _();
      });
    }));
  }
  const F = {
    set: y,
    update: (q, L) => y(q(c, l), L),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return F;
}
const {
  SvelteComponent: Cl,
  append: U,
  attr: C,
  component_subscribe: Ye,
  detach: Fl,
  element: Ml,
  init: Ll,
  insert: Nl,
  noop: Ge,
  safe_not_equal: zl,
  set_style: ve,
  svg_element: X,
  toggle_class: Oe
} = window.__gradio__svelte__internal, { onMount: Vl } = window.__gradio__svelte__internal;
function Kl(l) {
  let e, t, n, i, f, s, r, o, a, c, u, p;
  return {
    c() {
      e = Ml("div"), t = X("svg"), n = X("g"), i = X("path"), f = X("path"), s = X("path"), r = X("path"), o = X("g"), a = X("path"), c = X("path"), u = X("path"), p = X("path"), C(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), C(i, "fill", "#FF7C00"), C(i, "fill-opacity", "0.4"), C(i, "class", "svelte-43sxxs"), C(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), C(f, "fill", "#FF7C00"), C(f, "class", "svelte-43sxxs"), C(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), C(s, "fill", "#FF7C00"), C(s, "fill-opacity", "0.4"), C(s, "class", "svelte-43sxxs"), C(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), C(r, "fill", "#FF7C00"), C(r, "class", "svelte-43sxxs"), ve(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), C(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), C(a, "fill", "#FF7C00"), C(a, "fill-opacity", "0.4"), C(a, "class", "svelte-43sxxs"), C(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), C(c, "fill", "#FF7C00"), C(c, "class", "svelte-43sxxs"), C(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), C(u, "fill", "#FF7C00"), C(u, "fill-opacity", "0.4"), C(u, "class", "svelte-43sxxs"), C(p, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), C(p, "fill", "#FF7C00"), C(p, "class", "svelte-43sxxs"), ve(o, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), C(t, "viewBox", "-1200 -1200 3000 3000"), C(t, "fill", "none"), C(t, "xmlns", "http://www.w3.org/2000/svg"), C(t, "class", "svelte-43sxxs"), C(e, "class", "svelte-43sxxs"), Oe(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(h, y) {
      Nl(h, e, y), U(e, t), U(t, n), U(n, i), U(n, f), U(n, s), U(n, r), U(t, o), U(o, a), U(o, c), U(o, u), U(o, p);
    },
    p(h, [y]) {
      y & /*$top*/
      2 && ve(n, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), y & /*$bottom*/
      4 && ve(o, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), y & /*margin*/
      1 && Oe(
        e,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: Ge,
    o: Ge,
    d(h) {
      h && Fl(e);
    }
  };
}
function Sl(l, e, t) {
  let n, i;
  var f = this && this.__awaiter || function(h, y, F, q) {
    function L(d) {
      return d instanceof F ? d : new F(function(_) {
        _(d);
      });
    }
    return new (F || (F = Promise))(function(d, _) {
      function v(z) {
        try {
          b(q.next(z));
        } catch (S) {
          _(S);
        }
      }
      function V(z) {
        try {
          b(q.throw(z));
        } catch (S) {
          _(S);
        }
      }
      function b(z) {
        z.done ? d(z.value) : L(z.value).then(v, V);
      }
      b((q = q.apply(h, y || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const r = Xe([0, 0]);
  Ye(l, r, (h) => t(1, n = h));
  const o = Xe([0, 0]);
  Ye(l, o, (h) => t(2, i = h));
  let a;
  function c() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), o.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), o.set([125, -140])]), yield Promise.all([r.set([-125, 0]), o.set([125, -0])]), yield Promise.all([r.set([125, 0]), o.set([-125, 0])]);
    });
  }
  function u() {
    return f(this, void 0, void 0, function* () {
      yield c(), a || u();
    });
  }
  function p() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), o.set([-125, 0])]), u();
    });
  }
  return Vl(() => (p(), () => a = !0)), l.$$set = (h) => {
    "margin" in h && t(0, s = h.margin);
  }, [s, n, i, r, o];
}
class Al extends Cl {
  constructor(e) {
    super(), Ll(this, e, Sl, Kl, zl, { margin: 0 });
  }
}
const {
  SvelteComponent: Il,
  append: ce,
  attr: G,
  binding_callbacks: He,
  check_outros: Be,
  create_component: yt,
  create_slot: vt,
  destroy_component: qt,
  destroy_each: Ct,
  detach: w,
  element: x,
  empty: be,
  ensure_array_like: Fe,
  get_all_dirty_from_scope: Ft,
  get_slot_changes: Mt,
  group_outros: Ee,
  init: Zl,
  insert: k,
  mount_component: Lt,
  noop: De,
  safe_not_equal: jl,
  set_data: R,
  set_style: oe,
  space: W,
  text: M,
  toggle_class: P,
  transition_in: Y,
  transition_out: $,
  update_slot_base: Nt
} = window.__gradio__svelte__internal, { tick: Bl } = window.__gradio__svelte__internal, { onDestroy: El } = window.__gradio__svelte__internal, { createEventDispatcher: Dl } = window.__gradio__svelte__internal, Pl = (l) => ({}), Je = (l) => ({}), Wl = (l) => ({}), Qe = (l) => ({});
function xe(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function $e(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Rl(l) {
  let e, t, n, i, f = (
    /*i18n*/
    l[1]("common.error") + ""
  ), s, r, o;
  t = new _l({
    props: {
      Icon: kl,
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
  ), c = vt(
    a,
    l,
    /*$$scope*/
    l[29],
    Je
  );
  return {
    c() {
      e = x("div"), yt(t.$$.fragment), n = W(), i = x("span"), s = M(f), r = W(), c && c.c(), G(e, "class", "clear-status svelte-16nch4a"), G(i, "class", "error svelte-16nch4a");
    },
    m(u, p) {
      k(u, e, p), Lt(t, e, null), k(u, n, p), k(u, i, p), ce(i, s), k(u, r, p), c && c.m(u, p), o = !0;
    },
    p(u, p) {
      const h = {};
      p[0] & /*i18n*/
      2 && (h.label = /*i18n*/
      u[1]("common.clear")), t.$set(h), (!o || p[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      u[1]("common.error") + "") && R(s, f), c && c.p && (!o || p[0] & /*$$scope*/
      536870912) && Nt(
        c,
        a,
        u,
        /*$$scope*/
        u[29],
        o ? Mt(
          a,
          /*$$scope*/
          u[29],
          p,
          Pl
        ) : Ft(
          /*$$scope*/
          u[29]
        ),
        Je
      );
    },
    i(u) {
      o || (Y(t.$$.fragment, u), Y(c, u), o = !0);
    },
    o(u) {
      $(t.$$.fragment, u), $(c, u), o = !1;
    },
    d(u) {
      u && (w(e), w(n), w(i), w(r)), qt(t), c && c.d(u);
    }
  };
}
function Tl(l) {
  let e, t, n, i, f, s, r, o, a, c = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && et(l)
  );
  function u(_, v) {
    if (
      /*progress*/
      _[7]
    ) return Yl;
    if (
      /*queue_position*/
      _[2] !== null && /*queue_size*/
      _[3] !== void 0 && /*queue_position*/
      _[2] >= 0
    ) return Xl;
    if (
      /*queue_position*/
      _[2] === 0
    ) return Ul;
  }
  let p = u(l), h = p && p(l), y = (
    /*timer*/
    l[5] && nt(l)
  );
  const F = [Jl, Hl], q = [];
  function L(_, v) {
    return (
      /*last_progress_level*/
      _[15] != null ? 0 : (
        /*show_progress*/
        _[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = L(l)) && (s = q[f] = F[f](l));
  let d = !/*timer*/
  l[5] && ct(l);
  return {
    c() {
      c && c.c(), e = W(), t = x("div"), h && h.c(), n = W(), y && y.c(), i = W(), s && s.c(), r = W(), d && d.c(), o = be(), G(t, "class", "progress-text svelte-16nch4a"), P(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), P(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(_, v) {
      c && c.m(_, v), k(_, e, v), k(_, t, v), h && h.m(t, null), ce(t, n), y && y.m(t, null), k(_, i, v), ~f && q[f].m(_, v), k(_, r, v), d && d.m(_, v), k(_, o, v), a = !0;
    },
    p(_, v) {
      /*variant*/
      _[8] === "default" && /*show_eta_bar*/
      _[18] && /*show_progress*/
      _[6] === "full" ? c ? c.p(_, v) : (c = et(_), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), p === (p = u(_)) && h ? h.p(_, v) : (h && h.d(1), h = p && p(_), h && (h.c(), h.m(t, n))), /*timer*/
      _[5] ? y ? y.p(_, v) : (y = nt(_), y.c(), y.m(t, null)) : y && (y.d(1), y = null), (!a || v[0] & /*variant*/
      256) && P(
        t,
        "meta-text-center",
        /*variant*/
        _[8] === "center"
      ), (!a || v[0] & /*variant*/
      256) && P(
        t,
        "meta-text",
        /*variant*/
        _[8] === "default"
      );
      let V = f;
      f = L(_), f === V ? ~f && q[f].p(_, v) : (s && (Ee(), $(q[V], 1, 1, () => {
        q[V] = null;
      }), Be()), ~f ? (s = q[f], s ? s.p(_, v) : (s = q[f] = F[f](_), s.c()), Y(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      _[5] ? d && (Ee(), $(d, 1, 1, () => {
        d = null;
      }), Be()) : d ? (d.p(_, v), v[0] & /*timer*/
      32 && Y(d, 1)) : (d = ct(_), d.c(), Y(d, 1), d.m(o.parentNode, o));
    },
    i(_) {
      a || (Y(s), Y(d), a = !0);
    },
    o(_) {
      $(s), $(d), a = !1;
    },
    d(_) {
      _ && (w(e), w(t), w(i), w(r), w(o)), c && c.d(_), h && h.d(), y && y.d(), ~f && q[f].d(_), d && d.d(_);
    }
  };
}
function et(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = x("div"), G(e, "class", "eta-bar svelte-16nch4a"), oe(e, "transform", t);
    },
    m(n, i) {
      k(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && oe(e, "transform", t);
    },
    d(n) {
      n && w(e);
    }
  };
}
function Ul(l) {
  let e;
  return {
    c() {
      e = M("processing |");
    },
    m(t, n) {
      k(t, e, n);
    },
    p: De,
    d(t) {
      t && w(e);
    }
  };
}
function Xl(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, f, s;
  return {
    c() {
      e = M("queue: "), n = M(t), i = M("/"), f = M(
        /*queue_size*/
        l[3]
      ), s = M(" |");
    },
    m(r, o) {
      k(r, e, o), k(r, n, o), k(r, i, o), k(r, f, o), k(r, s, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && R(n, t), o[0] & /*queue_size*/
      8 && R(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (w(e), w(n), w(i), w(f), w(s));
    }
  };
}
function Yl(l) {
  let e, t = Fe(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = lt($e(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = be();
    },
    m(i, f) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, f);
      k(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Fe(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = $e(i, t, s);
          n[s] ? n[s].p(r, f) : (n[s] = lt(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && w(e), Ct(n, i);
    }
  };
}
function tt(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, f = " ", s;
  function r(c, u) {
    return (
      /*p*/
      c[41].length != null ? Ol : Gl
    );
  }
  let o = r(l), a = o(l);
  return {
    c() {
      a.c(), e = W(), n = M(t), i = M(" | "), s = M(f);
    },
    m(c, u) {
      a.m(c, u), k(c, e, u), k(c, n, u), k(c, i, u), k(c, s, u);
    },
    p(c, u) {
      o === (o = r(c)) && a ? a.p(c, u) : (a.d(1), a = o(c), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[41].unit + "") && R(n, t);
    },
    d(c) {
      c && (w(e), w(n), w(i), w(s)), a.d(c);
    }
  };
}
function Gl(l) {
  let e = me(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = M(e);
    },
    m(n, i) {
      k(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        n[41].index || 0
      ) + "") && R(t, e);
    },
    d(n) {
      n && w(t);
    }
  };
}
function Ol(l) {
  let e = me(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = me(
    /*p*/
    l[41].length
  ) + "", f;
  return {
    c() {
      t = M(e), n = M("/"), f = M(i);
    },
    m(s, r) {
      k(s, t, r), k(s, n, r), k(s, f, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        s[41].index || 0
      ) + "") && R(t, e), r[0] & /*progress*/
      128 && i !== (i = me(
        /*p*/
        s[41].length
      ) + "") && R(f, i);
    },
    d(s) {
      s && (w(t), w(n), w(f));
    }
  };
}
function lt(l) {
  let e, t = (
    /*p*/
    l[41].index != null && tt(l)
  );
  return {
    c() {
      t && t.c(), e = be();
    },
    m(n, i) {
      t && t.m(n, i), k(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = tt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && w(e), t && t.d(n);
    }
  };
}
function nt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = M(
        /*formatted_timer*/
        l[20]
      ), n = M(t), i = M("s");
    },
    m(f, s) {
      k(f, e, s), k(f, n, s), k(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && R(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && R(n, t);
    },
    d(f) {
      f && (w(e), w(n), w(i));
    }
  };
}
function Hl(l) {
  let e, t;
  return e = new Al({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      yt(e.$$.fragment);
    },
    m(n, i) {
      Lt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), e.$set(f);
    },
    i(n) {
      t || (Y(e.$$.fragment, n), t = !0);
    },
    o(n) {
      $(e.$$.fragment, n), t = !1;
    },
    d(n) {
      qt(e, n);
    }
  };
}
function Jl(l) {
  let e, t, n, i, f, s = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && it(l)
  );
  return {
    c() {
      e = x("div"), t = x("div"), r && r.c(), n = W(), i = x("div"), f = x("div"), G(t, "class", "progress-level-inner svelte-16nch4a"), G(f, "class", "progress-bar svelte-16nch4a"), oe(f, "width", s), G(i, "class", "progress-bar-wrap svelte-16nch4a"), G(e, "class", "progress-level svelte-16nch4a");
    },
    m(o, a) {
      k(o, e, a), ce(e, t), r && r.m(t, null), ce(e, n), ce(e, i), ce(i, f), l[31](f);
    },
    p(o, a) {
      /*progress*/
      o[7] != null ? r ? r.p(o, a) : (r = it(o), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      o[15] * 100}%`) && oe(f, "width", s);
    },
    i: De,
    o: De,
    d(o) {
      o && w(e), r && r.d(), l[31](null);
    }
  };
}
function it(l) {
  let e, t = Fe(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = rt(xe(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = be();
    },
    m(i, f) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, f);
      k(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Fe(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = xe(i, t, s);
          n[s] ? n[s].p(r, f) : (n[s] = rt(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && w(e), Ct(n, i);
    }
  };
}
function ft(l) {
  let e, t, n, i, f = (
    /*i*/
    l[43] !== 0 && Ql()
  ), s = (
    /*p*/
    l[41].desc != null && st(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && ot()
  ), o = (
    /*progress_level*/
    l[14] != null && at(l)
  );
  return {
    c() {
      f && f.c(), e = W(), s && s.c(), t = W(), r && r.c(), n = W(), o && o.c(), i = be();
    },
    m(a, c) {
      f && f.m(a, c), k(a, e, c), s && s.m(a, c), k(a, t, c), r && r.m(a, c), k(a, n, c), o && o.m(a, c), k(a, i, c);
    },
    p(a, c) {
      /*p*/
      a[41].desc != null ? s ? s.p(a, c) : (s = st(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = ot(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? o ? o.p(a, c) : (o = at(a), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(a) {
      a && (w(e), w(t), w(n), w(i)), f && f.d(a), s && s.d(a), r && r.d(a), o && o.d(a);
    }
  };
}
function Ql(l) {
  let e;
  return {
    c() {
      e = M(" /");
    },
    m(t, n) {
      k(t, e, n);
    },
    d(t) {
      t && w(e);
    }
  };
}
function st(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = M(e);
    },
    m(n, i) {
      k(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && R(t, e);
    },
    d(n) {
      n && w(t);
    }
  };
}
function ot(l) {
  let e;
  return {
    c() {
      e = M("-");
    },
    m(t, n) {
      k(t, e, n);
    },
    d(t) {
      t && w(e);
    }
  };
}
function at(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = M(e), n = M("%");
    },
    m(i, f) {
      k(i, t, f), k(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && R(t, e);
    },
    d(i) {
      i && (w(t), w(n));
    }
  };
}
function rt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && ft(l)
  );
  return {
    c() {
      t && t.c(), e = be();
    },
    m(n, i) {
      t && t.m(n, i), k(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = ft(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && w(e), t && t.d(n);
    }
  };
}
function ct(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), s = vt(
    f,
    l,
    /*$$scope*/
    l[29],
    Qe
  );
  return {
    c() {
      e = x("p"), t = M(
        /*loading_text*/
        l[9]
      ), n = W(), s && s.c(), G(e, "class", "loading svelte-16nch4a");
    },
    m(r, o) {
      k(r, e, o), ce(e, t), k(r, n, o), s && s.m(r, o), i = !0;
    },
    p(r, o) {
      (!i || o[0] & /*loading_text*/
      512) && R(
        t,
        /*loading_text*/
        r[9]
      ), s && s.p && (!i || o[0] & /*$$scope*/
      536870912) && Nt(
        s,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Mt(
          f,
          /*$$scope*/
          r[29],
          o,
          Wl
        ) : Ft(
          /*$$scope*/
          r[29]
        ),
        Qe
      );
    },
    i(r) {
      i || (Y(s, r), i = !0);
    },
    o(r) {
      $(s, r), i = !1;
    },
    d(r) {
      r && (w(e), w(n)), s && s.d(r);
    }
  };
}
function xl(l) {
  let e, t, n, i, f;
  const s = [Tl, Rl], r = [];
  function o(a, c) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = o(l)) && (n = r[t] = s[t](l)), {
    c() {
      e = x("div"), n && n.c(), G(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-16nch4a"), P(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), P(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), P(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), P(
        e,
        "border",
        /*border*/
        l[12]
      ), oe(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), oe(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, c) {
      k(a, e, c), ~t && r[t].m(e, null), l[33](e), f = !0;
    },
    p(a, c) {
      let u = t;
      t = o(a), t === u ? ~t && r[t].p(a, c) : (n && (Ee(), $(r[u], 1, 1, () => {
        r[u] = null;
      }), Be()), ~t ? (n = r[t], n ? n.p(a, c) : (n = r[t] = s[t](a), n.c()), Y(n, 1), n.m(e, null)) : n = null), (!f || c[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-16nch4a")) && G(e, "class", i), (!f || c[0] & /*variant, show_progress, status, show_progress*/
      336) && P(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && P(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || c[0] & /*variant, show_progress, status*/
      336) && P(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || c[0] & /*variant, show_progress, border*/
      4416) && P(
        e,
        "border",
        /*border*/
        a[12]
      ), c[0] & /*absolute*/
      1024 && oe(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && oe(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (Y(n), f = !0);
    },
    o(a) {
      $(n), f = !1;
    },
    d(a) {
      a && w(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var $l = function(l, e, t, n) {
  function i(f) {
    return f instanceof t ? f : new t(function(s) {
      s(f);
    });
  }
  return new (t || (t = Promise))(function(f, s) {
    function r(c) {
      try {
        a(n.next(c));
      } catch (u) {
        s(u);
      }
    }
    function o(c) {
      try {
        a(n.throw(c));
      } catch (u) {
        s(u);
      }
    }
    function a(c) {
      c.done ? f(c.value) : i(c.value).then(r, o);
    }
    a((n = n.apply(l, e || [])).next());
  });
};
let qe = [], Se = !1;
function en(l) {
  return $l(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (qe.push(e), !Se) Se = !0;
      else return;
      yield Bl(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < qe.length; i++) {
          const s = qe[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= n[0]) && (n[0] = s.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Se = !1, qe = [];
      });
    }
  });
}
function tn(l, e, t) {
  let n, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const s = Dl();
  let { i18n: r } = e, { eta: o = null } = e, { queue_position: a } = e, { queue_size: c } = e, { status: u } = e, { scroll_to_output: p = !1 } = e, { timer: h = !0 } = e, { show_progress: y = "full" } = e, { message: F = null } = e, { progress: q = null } = e, { variant: L = "default" } = e, { loading_text: d = "Loading..." } = e, { absolute: _ = !0 } = e, { translucent: v = !1 } = e, { border: V = !1 } = e, { autoscroll: b } = e, z, S = !1, ee = 0, te = 0, ie = null, fe = null, A = 0, Z = null, ae, O = null, m = !0;
  const K = () => {
    t(0, o = t(27, ie = t(19, le = null))), t(25, ee = performance.now()), t(26, te = 0), S = !0, j();
  };
  function j() {
    requestAnimationFrame(() => {
      t(26, te = (performance.now() - ee) / 1e3), S && j();
    });
  }
  function B() {
    t(26, te = 0), t(0, o = t(27, ie = t(19, le = null))), S && (S = !1);
  }
  El(() => {
    S && B();
  });
  let le = null;
  function H(g) {
    He[g ? "unshift" : "push"](() => {
      O = g, t(16, O), t(7, q), t(14, Z), t(15, ae);
    });
  }
  const ue = () => {
    s("clear_status");
  };
  function Le(g) {
    He[g ? "unshift" : "push"](() => {
      z = g, t(13, z);
    });
  }
  return l.$$set = (g) => {
    "i18n" in g && t(1, r = g.i18n), "eta" in g && t(0, o = g.eta), "queue_position" in g && t(2, a = g.queue_position), "queue_size" in g && t(3, c = g.queue_size), "status" in g && t(4, u = g.status), "scroll_to_output" in g && t(22, p = g.scroll_to_output), "timer" in g && t(5, h = g.timer), "show_progress" in g && t(6, y = g.show_progress), "message" in g && t(23, F = g.message), "progress" in g && t(7, q = g.progress), "variant" in g && t(8, L = g.variant), "loading_text" in g && t(9, d = g.loading_text), "absolute" in g && t(10, _ = g.absolute), "translucent" in g && t(11, v = g.translucent), "border" in g && t(12, V = g.border), "autoscroll" in g && t(24, b = g.autoscroll), "$$scope" in g && t(29, f = g.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (o === null && t(0, o = ie), o != null && ie !== o && (t(28, fe = (performance.now() - ee) / 1e3 + o), t(19, le = fe.toFixed(1)), t(27, ie = o))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, A = fe === null || fe <= 0 || !te ? null : Math.min(te / fe, 1)), l.$$.dirty[0] & /*progress*/
    128 && q != null && t(18, m = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (q != null ? t(14, Z = q.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : t(14, Z = null), Z ? (t(15, ae = Z[Z.length - 1]), O && (ae === 0 ? t(16, O.style.transition = "0", O) : t(16, O.style.transition = "150ms", O))) : t(15, ae = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? K() : B()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && z && p && (u === "pending" || u === "complete") && en(z, b), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = te.toFixed(1));
  }, [
    o,
    r,
    a,
    c,
    u,
    h,
    y,
    q,
    L,
    d,
    _,
    v,
    V,
    z,
    Z,
    ae,
    O,
    A,
    m,
    le,
    n,
    s,
    p,
    F,
    b,
    ee,
    te,
    ie,
    fe,
    f,
    i,
    H,
    ue,
    Le
  ];
}
class ln extends Il {
  constructor(e) {
    super(), Zl(
      this,
      e,
      tn,
      xl,
      jl,
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
const {
  SvelteComponent: nn,
  assign: fn,
  attr: Ae,
  binding_callbacks: sn,
  check_outros: on,
  create_component: zt,
  destroy_component: Vt,
  detach: ut,
  element: an,
  flush: N,
  get_spread_object: rn,
  get_spread_update: cn,
  group_outros: un,
  init: _n,
  insert: _t,
  mount_component: Kt,
  safe_not_equal: dn,
  space: mn,
  src_url_equal: hn,
  transition_in: ke,
  transition_out: Me
} = window.__gradio__svelte__internal, { onMount: bn } = window.__gradio__svelte__internal, { tick: gn } = window.__gradio__svelte__internal;
function dt(l) {
  let e, t;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[0].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[0].i18n
    ) },
    /*loading_status*/
    l[6]
  ];
  let i = {};
  for (let f = 0; f < n.length; f += 1)
    i = fn(i, n[f]);
  return e = new ln({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[21]
  ), {
    c() {
      zt(e.$$.fragment);
    },
    m(f, s) {
      Kt(e, f, s), t = !0;
    },
    p(f, s) {
      const r = s[0] & /*gradio, loading_status*/
      65 ? cn(n, [
        s[0] & /*gradio*/
        1 && { autoscroll: (
          /*gradio*/
          f[0].autoscroll
        ) },
        s[0] & /*gradio*/
        1 && { i18n: (
          /*gradio*/
          f[0].i18n
        ) },
        s[0] & /*loading_status*/
        64 && rn(
          /*loading_status*/
          f[6]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (ke(e.$$.fragment, f), t = !0);
    },
    o(f) {
      Me(e.$$.fragment, f), t = !1;
    },
    d(f) {
      Vt(e, f);
    }
  };
}
function wn(l) {
  let e, t, n, i, f, s = (
    /*loading_status*/
    l[6] && dt(l)
  );
  return {
    c() {
      s && s.c(), e = mn(), t = an("iframe"), hn(t.src, n = "https://bohrium.dp.tech/app/function-panel") || Ae(t, "src", n), Ae(t, "style", i = "width:" + /*width*/
      l[7] + "px;height: " + /*height*/
      l[8] + "px;padding: 24px;background: #ffffff;" + /*visible*/
      (l[3] ? "" : "display: none;"));
    },
    m(r, o) {
      s && s.m(r, o), _t(r, e, o), _t(r, t, o), l[22](t), f = !0;
    },
    p(r, o) {
      /*loading_status*/
      r[6] ? s ? (s.p(r, o), o[0] & /*loading_status*/
      64 && ke(s, 1)) : (s = dt(r), s.c(), ke(s, 1), s.m(e.parentNode, e)) : s && (un(), Me(s, 1, 1, () => {
        s = null;
      }), on()), (!f || o[0] & /*width, height, visible*/
      392 && i !== (i = "width:" + /*width*/
      r[7] + "px;height: " + /*height*/
      r[8] + "px;padding: 24px;background: #ffffff;" + /*visible*/
      (r[3] ? "" : "display: none;"))) && Ae(t, "style", i);
    },
    i(r) {
      f || (ke(s), f = !0);
    },
    o(r) {
      Me(s), f = !1;
    },
    d(r) {
      r && (ut(e), ut(t)), s && s.d(r), l[22](null);
    }
  };
}
function kn(l) {
  let e, t;
  return e = new Jt({
    props: {
      visible: (
        /*visible*/
        l[3]
      ),
      elem_id: (
        /*elem_id*/
        l[1]
      ),
      elem_classes: (
        /*elem_classes*/
        l[2]
      ),
      scale: (
        /*scale*/
        l[4]
      ),
      min_width: (
        /*min_width*/
        l[5]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [wn] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      zt(e.$$.fragment);
    },
    m(n, i) {
      Kt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*visible*/
      8 && (f.visible = /*visible*/
      n[3]), i[0] & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      n[1]), i[0] & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      n[2]), i[0] & /*scale*/
      16 && (f.scale = /*scale*/
      n[4]), i[0] & /*min_width*/
      32 && (f.min_width = /*min_width*/
      n[5]), i[0] & /*width, height, visible, iframeRef, gradio, loading_status*/
      969 | i[1] & /*$$scope*/
      1 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (ke(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Me(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Vt(e, n);
    }
  };
}
function pn(l, e, t) {
  var n = this && this.__awaiter || function(m, K, j, B) {
    function le(H) {
      return H instanceof j ? H : new j(function(ue) {
        ue(H);
      });
    }
    return new (j || (j = Promise))(function(H, ue) {
      function Le(D) {
        try {
          ge(B.next(D));
        } catch (se) {
          ue(se);
        }
      }
      function g(D) {
        try {
          ge(B.throw(D));
        } catch (se) {
          ue(se);
        }
      }
      function ge(D) {
        D.done ? H(D.value) : le(D.value).then(Le, g);
      }
      ge((B = B.apply(m, K || [])).next());
    });
  };
  let { gradio: i } = e, { label: f = "Textbox" } = e, { elem_id: s = "" } = e, { elem_classes: r = [] } = e, { visible: o = !0 } = e, { value: a = "" } = e, { placeholder: c = "" } = e, { show_label: u } = e, { scale: p = null } = e, { min_width: h = void 0 } = e, { loading_status: y = void 0 } = e, { value_is_output: F = !1 } = e, { interactive: q } = e, { rtl: L = !1 } = e, { width: d } = e, { height: _ } = e, { accept: v } = e, { appKey: V } = e, { appAccessKey: b } = e, { clientName: z } = e, S, ee;
  function te() {
    let m = /* @__PURE__ */ new Map();
    document.cookie.split(";").forEach((K) => {
      const [j, B] = K.trim().split("=");
      m.set(j, B);
    }), S = b ?? m.get("appAccessKey"), ee = z ?? m.get("clientName");
  }
  function ie() {
    i.dispatch("change"), F || i.dispatch("input");
  }
  function fe() {
    return n(this, void 0, void 0, function* () {
      yield gn(), i.dispatch("submit");
    });
  }
  let A;
  const Z = () => {
    var m, K, j, B;
    const le = (K = (m = window.location.search.match(/deploymentId=([^&]*)/)) === null || m === void 0 ? void 0 : m[1]) !== null && K !== void 0 ? K : "", H = (B = (j = window.location.search.match(/mode=([^&]*)/)) === null || j === void 0 ? void 0 : j[1]) !== null && B !== void 0 ? B : "";
    V && (A != null && A.contentWindow) && A.contentWindow.postMessage(
      {
        id: "1",
        type: "selectFromBohrium",
        data: {
          accept: v,
          appKey: V,
          deploymentId: le ? +le : void 0,
          scene: H || void 0,
          directory: !1
        },
        headers: { accessKey: S, "x-app-key": ee }
      },
      "*"
    );
  };
  bn(() => {
    te(), t(
      9,
      A.onload = () => {
        Z();
      },
      A
    ), window.addEventListener("message", function(m) {
      return n(this, void 0, void 0, function* () {
        const { data: K } = m;
        K.type === "selectFromBohrium" && K.status === "succeed" && (t(10, a = encodeURI(decodeURIComponent(K.data.url))), A.contentWindow.postMessage(
          {
            id: "1",
            type: "clear",
            data: {},
            headers: { accessKey: S, "x-app-key": ee }
          },
          "*"
        )), K.type === "closeWindow" && (fe(), A.contentWindow.postMessage(
          {
            id: "1",
            type: "clear",
            data: {},
            headers: { accessKey: S, "x-app-key": ee }
          },
          "*"
        )), K.type === "ready" && Z();
      });
    });
  });
  const ae = () => i.dispatch("clear_status", y);
  function O(m) {
    sn[m ? "unshift" : "push"](() => {
      A = m, t(9, A);
    });
  }
  return l.$$set = (m) => {
    "gradio" in m && t(0, i = m.gradio), "label" in m && t(11, f = m.label), "elem_id" in m && t(1, s = m.elem_id), "elem_classes" in m && t(2, r = m.elem_classes), "visible" in m && t(3, o = m.visible), "value" in m && t(10, a = m.value), "placeholder" in m && t(12, c = m.placeholder), "show_label" in m && t(13, u = m.show_label), "scale" in m && t(4, p = m.scale), "min_width" in m && t(5, h = m.min_width), "loading_status" in m && t(6, y = m.loading_status), "value_is_output" in m && t(14, F = m.value_is_output), "interactive" in m && t(15, q = m.interactive), "rtl" in m && t(16, L = m.rtl), "width" in m && t(7, d = m.width), "height" in m && t(8, _ = m.height), "accept" in m && t(17, v = m.accept), "appKey" in m && t(18, V = m.appKey), "appAccessKey" in m && t(19, b = m.appAccessKey), "clientName" in m && t(20, z = m.clientName);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1024 && a === null && t(10, a = ""), l.$$.dirty[0] & /*value*/
    1024 && ie(), l.$$.dirty[0] & /*accept*/
    131072 && Z(), l.$$.dirty[0] & /*appKey*/
    262144 && Z(), l.$$.dirty[0] & /*visible*/
    8 && Z();
  }, [
    i,
    s,
    r,
    o,
    p,
    h,
    y,
    d,
    _,
    A,
    a,
    f,
    c,
    u,
    F,
    q,
    L,
    v,
    V,
    b,
    z,
    ae,
    O
  ];
}
class yn extends nn {
  constructor(e) {
    super(), _n(
      this,
      e,
      pn,
      kn,
      dn,
      {
        gradio: 0,
        label: 11,
        elem_id: 1,
        elem_classes: 2,
        visible: 3,
        value: 10,
        placeholder: 12,
        show_label: 13,
        scale: 4,
        min_width: 5,
        loading_status: 6,
        value_is_output: 14,
        interactive: 15,
        rtl: 16,
        width: 7,
        height: 8,
        accept: 17,
        appKey: 18,
        appAccessKey: 19,
        clientName: 20
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[0];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), N();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(e) {
    this.$$set({ label: e }), N();
  }
  get elem_id() {
    return this.$$.ctx[1];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), N();
  }
  get elem_classes() {
    return this.$$.ctx[2];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), N();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(e) {
    this.$$set({ visible: e }), N();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(e) {
    this.$$set({ value: e }), N();
  }
  get placeholder() {
    return this.$$.ctx[12];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), N();
  }
  get show_label() {
    return this.$$.ctx[13];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), N();
  }
  get scale() {
    return this.$$.ctx[4];
  }
  set scale(e) {
    this.$$set({ scale: e }), N();
  }
  get min_width() {
    return this.$$.ctx[5];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), N();
  }
  get loading_status() {
    return this.$$.ctx[6];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), N();
  }
  get value_is_output() {
    return this.$$.ctx[14];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), N();
  }
  get interactive() {
    return this.$$.ctx[15];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), N();
  }
  get rtl() {
    return this.$$.ctx[16];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), N();
  }
  get width() {
    return this.$$.ctx[7];
  }
  set width(e) {
    this.$$set({ width: e }), N();
  }
  get height() {
    return this.$$.ctx[8];
  }
  set height(e) {
    this.$$set({ height: e }), N();
  }
  get accept() {
    return this.$$.ctx[17];
  }
  set accept(e) {
    this.$$set({ accept: e }), N();
  }
  get appKey() {
    return this.$$.ctx[18];
  }
  set appKey(e) {
    this.$$set({ appKey: e }), N();
  }
  get appAccessKey() {
    return this.$$.ctx[19];
  }
  set appAccessKey(e) {
    this.$$set({ appAccessKey: e }), N();
  }
  get clientName() {
    return this.$$.ctx[20];
  }
  set clientName(e) {
    this.$$set({ clientName: e }), N();
  }
}
export {
  yn as default
};
