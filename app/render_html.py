import streamlit as st


CSS = """
<link rel="stylesheet"
      href="/app/static/stylesheets/moj-frontend.min.css">
<link rel="stylesheet"
      href="/app/static/stylesheets/govuk-frontend-5.1.0.min.css">

<style>
  .moj-header,
  .govuk-footer {
      margin-left: -6rem;
      margin-right: -6rem;
  }

  .govuk-footer {
      margin-top: 3rem;
  }

  .block-container {
      padding-top: 1rem;
  }
</style>
"""


def render_header() -> None:
    st.markdown(
        CSS
        + """
<header class="moj-header" role="banner">
  <div class="moj-header__container">
    <div class="moj-header__logo">
      <img
        src="/app/static/images/moj-logotype-crest.png"
        alt=""
        width="40"
        height="40"
        class="moj-header__logotype-crest"
      >
      <a
        class="moj-header__link moj-header__link--organisation-name"
        href="#"
      >
        Ministry of Justice
      </a>
      <a
        class="moj-header__link moj-header__link--service-name"
        href="/"
      >
        Cost Optimisation Hub Dashboard
      </a>
    </div>
  </div>
</header>
""",
        unsafe_allow_html=True,
    )


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