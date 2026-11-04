# daisyUI Card and Button

Official daisyUI 5.7.50 components compiled with Tailwind CSS.

- Card: https://daisyui.com/components/card/
- Button: https://daisyui.com/components/button/
- Exact dependencies: build-package.json and build-package-lock.json
- Build input: card.input.css
- Version, npm integrity and generated CSS hash: provenance.json
- Licenses: LICENSE.daisyui and LICENSE.tailwindcss

The component is inside a native declarative shadow root so the official Tailwind reset does not restyle Minimal's article content. card.css is the unedited compiler output. properties.css contains only the generated @property rules, repeated at document scope for browser compatibility. No card appearance is drawn by site CSS.

To rebuild in a temporary directory, install the exact build-package dependencies, compile card.input.css with the Tailwind CLI, and extract top-level @property rules into properties.css.
