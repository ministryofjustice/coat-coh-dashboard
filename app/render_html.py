import streamlit as st


CSS = """
<link rel="stylesheet" href="/app/static/stylesheets/moj-frontend.min.css">
<link rel="stylesheet" href="/app/static/stylesheets/govuk-frontend-5.1.0.min.css">

<style>
/* Replace Streamlit's fixed toolbar/header with the MoJ service header. */
[data-testid="stHeader"] {
  display: none;
}

[data-testid="stToolbar"] {
  display: none;
}

#moj-header-root {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 999999;
}

# [data-testid="stMainBlockContainer"] {
#   position: fixed;
#   top: 4.5rem;
#   height: calc(100vh - 4.5rem);
# }

/* The sidebar is itself a fixed-position element, so it must be offset
   using `top`/`height`, not `margin-top`, or it will render underneath
   the header instead of being pushed down by it. */
[data-testid="stSidebar"] {
  position: fixed;
  top: 4.5rem;
  height: calc(100vh - 4.5rem);
}

/* Allow the footer to span beyond the normal Streamlit content width. */
.govuk-footer {
  margin-top: 3rem;
  margin-left: -6rem;
  margin-right: -6rem;
}
</style>
"""


def render_header() -> None:
    HEADER_HTML = """
<div id="moj-header-root">
  <header class="moj-header" role="banner">
    <div class="moj-header__container">
      <div class="moj-header__logo">
        <img src="/app/static/images/moj-logotype-crest.png" alt=""
             width="40" height="40" class="moj-header__logotype-crest">
        <a class="moj-header__link moj-header__link--organisation-name" href="#">
          Ministry of Justice
        </a>
        <a class="moj-header__link moj-header__link--service-name" href="/">
          Cost Optimisation Hub Dashboard
        </a>
      </div>
    </div>
  </header>
</div>
"""

    st.markdown(CSS + HEADER_HTML, unsafe_allow_html=True,)


def render_footer() -> None:
    st.markdown(
        """
<footer class="govuk-footer" role="contentinfo">
  <div class="govuk-width-container">
    <div class="govuk-footer__meta">
      <div class="govuk-footer__meta-item govuk-footer__meta-item--grow">
        <h2 class="govuk-visually-hidden">Support links</h2>

        <ul class="govuk-footer__inline-list">
          <li class="govuk-footer__inline-list-item">
            <a class="govuk-footer__link" href="#">
              Ministry of Justice
            </a>
          </li>
        </ul>

        <span class="govuk-footer__licence-description">
          Built by the Ministry of Justice
        </span>
      </div>
    </div>
  </div>
</footer>
""",
        unsafe_allow_html=True,
    )