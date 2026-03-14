<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ManoGuzman/mpg-to-kml">
    <img src="https://img.icons8.com/?size=100&id=gic1MWHLgRmE&format=png&color=000000" alt="Fuel Logo" width="80" height="80">
  </a>

<h3 align="center">MPG to km/l — Fuel Cost Calculator</h3>

  <p align="center">
    A CLI tool that converts vehicle fuel efficiency from MPG to km/l and calculates trip fuel costs using live RECOPE gasoline prices for Costa Rica.
    <br />
    <a href="https://github.com/ManoGuzman/mpg-to-kml"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ManoGuzman/mpg-to-kml">View Demo</a>
    &middot;
    <a href="https://github.com/ManoGuzman/mpg-to-kml/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/ManoGuzman/mpg-to-kml/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

`mpg-to-kml` is an interactive CLI fuel cost calculator aimed at drivers in Costa Rica. Given a vehicle's fuel efficiency in **miles per gallon (MPG)** and a trip distance in **kilometers**, the tool:

1. Converts the efficiency to **km/l** (kilometers per liter) using the standard factor `0.425144`.
2. Scrapes the live **Super gasoline price in Costa Rican Colones (₡)** from the official [RECOPE](https://recope.go.cr) government website, with a hardcoded fallback of `₡697.00` if the site is unreachable.
3. Calculates and displays the **total fuel cost** for the trip.

**Example session:**

```
=== Calculadora de Costo de Combustible ===

Ingrese la eficiencia del vehículo (MPG): 30
Ingrese la distancia recorrida (kms): 100

==================================================
Eficiencia: 30.0 mpg = 12.75 km/l
Distancia recorrida: 100.0 km
Combustible consumido: 7.84 litros
Precio por litro: ₡750.00
Costo total: ₡5,882.35
==================================================
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![Requests][Requests-badge]][Requests-url]
* [![lxml][lxml-badge]][lxml-url]
* [![Pytest][Pytest-badge]][Pytest-url]
* [![Ruff][Ruff-badge]][Ruff-url]
* [![Black][Black-badge]][Black-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

* Python 3.8 or higher
* `pip`

```sh
python --version   # should be 3.8+
pip --version
```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ManoGuzman/mpg-to-kml.git
   cd mpg-to-kml
   ```

2. Install the package (runtime dependencies only)
   ```sh
   pip install .
   ```

3. Or install with development/test tools
   ```sh
   pip install ".[dev]"
   ```

4. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/mpg-to-kml
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Run the interactive CLI after installation:

```sh
mpg-to-kml
```

The tool will prompt you for:
- **MPG** — your vehicle's fuel efficiency in miles per gallon
- **Distance** — the trip distance in kilometers

It then fetches the current Super gasoline price from RECOPE and prints the full cost breakdown. If the RECOPE website is unavailable, it falls back to a default price of `₡697.00` and notifies you.

**Run the test suite:**

```sh
pytest
```

**Lint the source code:**

```sh
ruff check src/mpg_to_kml/
```

**Build a distributable package:**

```sh
pip install build twine
python -m build
twine check dist/*
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Support additional fuel grades (Regular, Diesel)
- [ ] Add flag-based CLI interface (argparse / Click) alongside the interactive mode
- [ ] Expose a public Python API for programmatic use
- [ ] Support multiple currencies / price sources beyond Costa Rica
    - [ ] USD support
    - [ ] EUR support

See the [open issues](https://github.com/ManoGuzman/mpg-to-kml/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/ManoGuzman/mpg-to-kml/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ManoGuzman/mpg-to-kml" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Manuel Guzman - [@LinkedIn](https://linkedin.com/in/manuel-guzmán-b87b841bb)

Project Link: [https://github.com/ManoGuzman/mpg-to-kml](https://github.com/ManoGuzman/mpg-to-kml)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [RECOPE](https://recope.go.cr) — Costa Rica's official fuel pricing authority
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — README template used as the base for this document
* [Icons8](https://icons8.com) — Project logo icon

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ManoGuzman/mpg-to-kml.svg?style=for-the-badge
[contributors-url]: https://github.com/ManoGuzman/mpg-to-kml/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ManoGuzman/mpg-to-kml.svg?style=for-the-badge
[forks-url]: https://github.com/ManoGuzman/mpg-to-kml/network/members
[stars-shield]: https://img.shields.io/github/stars/ManoGuzman/mpg-to-kml.svg?style=for-the-badge
[stars-url]: https://github.com/ManoGuzman/mpg-to-kml/stargazers
[issues-shield]: https://img.shields.io/github/issues/ManoGuzman/mpg-to-kml.svg?style=for-the-badge
[issues-url]: https://github.com/ManoGuzman/mpg-to-kml/issues
[license-shield]: https://img.shields.io/github/license/ManoGuzman/mpg-to-kml.svg?style=for-the-badge
[license-url]: https://github.com/ManoGuzman/mpg-to-kml/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/manuel-guzmán-b87b841bb
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Requests-badge]: https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white
[Requests-url]: https://requests.readthedocs.io/
[lxml-badge]: https://img.shields.io/badge/lxml-2F9C3A?style=for-the-badge&logo=xml&logoColor=white
[lxml-url]: https://lxml.de/
[Pytest-badge]: https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white
[Pytest-url]: https://docs.pytest.org/
[Ruff-badge]: https://img.shields.io/badge/Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black
[Ruff-url]: https://docs.astral.sh/ruff/
[Black-badge]: https://img.shields.io/badge/Black-000000?style=for-the-badge&logo=python&logoColor=white
[Black-url]: https://black.readthedocs.io/
