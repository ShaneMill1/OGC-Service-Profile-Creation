# Examples

## Basic Profile

Generate a simple profile with items query only:

```bash
python src/create_profile.py \
  --name "simple-profile" \
  --title "Simple EDR Profile" \
  --query-types items \
  --output ./simple-profile
```

## Multi-Query Profile

Generate a profile supporting multiple query types:

```bash
python src/create_profile.py \
  --name "weather-profile" \
  --title "Weather Data Profile" \
  --query-types items,position,area,radius \
  --output ./weather-profile \
  --author "Weather Service" \
  --email "weather@example.com"
```

## Water Gauge Profile

Real-world example - water gauge observations:

```bash
python src/create_profile.py \
  --name "water-gauge-profile" \
  --title "Water Gauge Profile" \
  --query-types items,position \
  --output ./water-gauge-profile \
  --author "NOAA/NWS/MDL" \
  --email "shane.mill@noaa.gov"
```

### Features

- Real-time water gauge observations
- Flood stage monitoring
- Station-based queries
- GeoJSON output

## Aviation Profile

Aviation weather observations:

```bash
python src/create_profile.py \
  --name "aviation-profile" \
  --title "Aviation Weather Profile" \
  --query-types items,position,radius,trajectory,corridor \
  --output ./aviation-profile
```

### Use Cases

- METAR/TAF observations
- Flight path weather
- Airport vicinity weather
- Route weather briefings

## Marine Profile

Marine and coastal observations:

```bash
python src/create_profile.py \
  --name "marine-profile" \
  --title "Marine Observations Profile" \
  --query-types items,position,area,trajectory \
  --output ./marine-profile
```

### Use Cases

- Buoy observations
- Coastal station data
- Ship route weather
- Marine zone forecasts

## Climate Profile

Climate data with temporal instances:

```bash
python src/create_profile.py \
  --name "climate-profile" \
  --title "Climate Data Profile" \
  --query-types items,position,area,cube,instances \
  --output ./climate-profile
```

### Use Cases

- Historical climate data
- Climate normals
- Temporal aggregations
- Multi-dimensional queries

## Customizing Generated Profiles

After generation, you can customize:

### 1. Requirements

Edit `requirements/requirements_class_*.adoc`:

```asciidoc
[requirement,uri="/req/my-profile/custom-requirement"]
====
[.component,class=part]
--
Custom requirement text here.
--
====
```

### 2. Tests

Edit `abstract_tests/test_*.adoc`:

```asciidoc
[abstract_test,uri="/conf/my-profile/custom-test"]
====
[.component,class=test method]
--
Test method description.
--

[.component,class=test purpose]
--
Test purpose.
--
====
```

### 3. Sections

Edit files in `sections/`:

- `00-preface.adoc` - Preface and acknowledgments
- `06-overview.adoc` - Profile overview
- `07-requirements.adoc` - Requirements overview

### 4. Build Configuration

Edit `Makefile` to customize build options:

```makefile
METANORMA_OPTS = --agree-to-terms -t ogc -x xml,html,pdf,doc
```

## Building Examples

```bash
# Build all examples
for profile in simple-profile weather-profile water-gauge-profile; do
  cd $profile
  make
  cd ..
done
```

## Validation

Validate generated profiles:

```bash
# Check AsciiDoc syntax
asciidoctor -o /dev/null document.adoc

# Build with Metanorma
make

# Check for errors
echo $?
```
