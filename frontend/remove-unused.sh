#!/bin/bash
# يحذف ملفات قالب Vue الافتراضية غير المستخدمة (تأكدت أنه لا يستورد أي منها شيء من التطبيق)
# شغّله من مجلد frontend:  bash remove-unused.sh
set -e
rm -rf src/components/HelloWorld.vue src/components/TheWelcome.vue \
       src/components/WelcomeItem.vue src/components/icons \
       src/views/AboutView.vue src/views/HomeView.vue \
       src/stores/counter.js src/assets/base.css src/assets/logo.svg README.md
echo "تم الحذف"
