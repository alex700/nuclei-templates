<?php

use Drupal\commerce_order\Entity\Order;
use Drupal\commerce_store\Entity\Store;
use Drupal\user\Entity\User;

$existing = \Drupal::entityTypeManager()->getStorage('user')->loadByProperties(['name' => 'labcustomer']);
if ($existing) {
  $customer = reset($existing);
}
else {
  $customer = User::create([
    'name' => 'labcustomer',
    'mail' => 'customer@example.invalid',
    'pass' => 'labpass123',
    'status' => 1,
  ]);
  $customer->save();
}

$stores = \Drupal::entityTypeManager()->getStorage('commerce_store')->loadMultiple();
if ($stores) {
  $store = reset($stores);
}
else {
  $store = Store::create([
    'type' => 'online',
    'name' => 'Lab store',
    'mail' => 'store@example.invalid',
    'address' => ['country_code' => 'US'],
    'default' => TRUE,
    'uid' => 1,
  ]);
  $store->save();
}

$orders = \Drupal::entityTypeManager()->getStorage('commerce_order')->loadByProperties(['uid' => $customer->id()]);
if ($orders) {
  $order = reset($orders);
}
else {
  $order = Order::create([
    'type' => 'default',
    'state' => 'draft',
    'store_id' => $store->id(),
    'uid' => $customer->id(),
    'cart' => TRUE,
  ]);
  $order->save();
}

echo json_encode([
  'customer_id' => $customer->id(),
  'store_id' => $store->id(),
  'order_id' => $order->id(),
  'customer_update_access' => $order->access('update', $customer),
], JSON_PRETTY_PRINT) . PHP_EOL;
