import { router } from "@web/core/browser/router";

const keys = [
  "add_fields",
  "highlight_fields",
  "order_by",
  "decoration_info",
  "decoration_muted",
  "decoration_success",
  "decoration_warning",
  "decoration_danger",
];

for (const key of keys) {
  router.addLockedKey(key);
}