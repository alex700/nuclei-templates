<?php
$site = $argv[1] ?? 'vulnerable';
$_SERVER['HTTP_HOST'] = $site;
$_SERVER['SERVER_NAME'] = $site;
$_SERVER['REQUEST_METHOD'] = 'GET';
define('WP_INSTALLING', true);
require '/var/www/html/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
require_once ABSPATH . 'wp-admin/includes/plugin.php';
if (!is_blog_installed()) {
    wp_install('Nuclei Elementor lab', 'labadmin', 'labadmin@example.invalid', true, '', 'LabPass_2026!', 'en_US');
}
if (!is_plugin_active('elementor/elementor.php')) {
    $result = activate_plugin('elementor/elementor.php');
    if (is_wp_error($result)) { fwrite(STDERR, $result->get_error_message() . "\n"); exit(1); }
}
update_option('elementor_experiment-editor_events', 'active');
$user = get_user_by('login', 'labadmin');
if (!$user) { fwrite(STDERR, "admin user missing\n"); exit(1); }
$expires = time() + 3600;
$session = WP_Session_Tokens::get_instance($user->ID)->create($expires);
$cookie_name = 'wordpress_logged_in_' . md5(get_option('siteurl'));
$cookie = $cookie_name . '=' . wp_generate_auth_cookie($user->ID, $expires, 'logged_in', $session);
file_put_contents('/lab-state/cookie.txt', $cookie . "\n");
echo json_encode(['site' => $site, 'plugin' => get_plugin_data(WP_PLUGIN_DIR.'/elementor/elementor.php')['Version'], 'user' => $user->ID]) . "\n";
