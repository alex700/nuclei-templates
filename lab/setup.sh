#!/usr/bin/env bash
set -euo pipefail

lab_dir="$(cd "$(dirname "$0")" && pwd)"
image='local/drupal-commerce-cve-2026-118539:base'

for variant in vulnerable patched legacy-vulnerable legacy-patched no-product later-product; do
  if [[ -e "$lab_dir/$variant" ]]; then
    echo "Refusing to replace existing $lab_dir/$variant" >&2
    exit 1
  fi
done

docker build -f "$lab_dir/Dockerfile.drupal" -t "$image" "$lab_dir"

for variant in vulnerable patched legacy-vulnerable legacy-patched; do
  mkdir "$lab_dir/$variant"
  case "$variant" in
    vulnerable) commerce_version='3.3.12' ;;
    patched) commerce_version='3.3.13' ;;
    legacy-vulnerable) commerce_version='2.40.0' ;;
    legacy-patched) commerce_version='2.41.0' ;;
  esac
  docker run --rm -e COMMERCE_VERSION="$commerce_version" \
    -v "$lab_dir/$variant:/workspace" -v "$lab_dir/locks/$variant:/locks:ro" \
    -v "$lab_dir/create-fixture.php:/fixture.php:ro" \
    -v "$lab_dir/create-public-product.php:/product-fixture.php:ro" \
    -w /workspace "$image" sh -ec '
      cp -a /opt/drupal/. /workspace/
      cp /locks/composer.json /locks/composer.lock /workspace/
      composer install --no-interaction --no-progress
      php -r '\''$j=json_decode(file_get_contents("composer.lock"), true); foreach ($j["packages"] as $p) { if ($p["name"] === "drupal/commerce") { exit($p["version"] === getenv("COMMERCE_VERSION") ? 0 : 1); }} exit(1);'\''
      vendor/bin/drush site:install standard --db-url=sqlite://default/files/lab.sqlite \
        --account-name=labadmin --account-pass=labadmin123 --site-name=CommerceLab -y
      vendor/bin/drush en commerce_cart commerce_store commerce_order commerce_product -y
      vendor/bin/drush php:script /fixture.php
      vendor/bin/drush php:script /product-fixture.php
      sed -i "s@/workspace/@/opt/drupal/@g" web/sites/default/settings.php
      db_file="$(find web -name lab.sqlite -print -quit)"
      test -n "$db_file"
      chmod 666 "$db_file"
      chmod 777 "$(dirname "$db_file")"
    '
done

cp -a "$lab_dir/vulnerable" "$lab_dir/no-product"
cp -a "$lab_dir/vulnerable" "$lab_dir/later-product"
for variant in no-product later-product; do
  docker run --rm -v "$lab_dir/$variant:/opt/drupal" -w /opt/drupal "$image" \
    vendor/bin/drush php:eval '\Drupal\commerce_product\Entity\Product::load(1)->setUnpublished()->save();'
done
docker run --rm -v "$lab_dir/later-product:/opt/drupal" \
  -v "$lab_dir/create-later-product.php:/later-product.php:ro" \
  -w /opt/drupal "$image" vendor/bin/drush php:script /later-product.php

echo 'Six isolated Commerce installations are prepared. Run tests/verify.py from the package root.'
