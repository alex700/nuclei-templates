<?php
use Drupal\commerce_product\Entity\Product;
use Drupal\commerce_product\Entity\ProductVariation;
use Drupal\commerce_price\Price;
$stores = \Drupal::entityTypeManager()->getStorage('commerce_store')->loadMultiple();
$store = reset($stores);
if (!$store) { throw new RuntimeException('No store'); }
$product = Product::create(['type' => 'default', 'title' => 'Guest cart probe item', 'stores' => [$store], 'status' => 1]);
$product->save();
$variation = ProductVariation::create(['type' => 'default', 'sku' => 'GUEST-CART-STEP-1', 'title' => 'Guest cart probe item', 'status' => 1, 'price' => new Price('12.00', 'USD')]);
$variation->save();
$product->addVariation($variation)->save();
echo 'product_id=' . $product->id() . PHP_EOL;
