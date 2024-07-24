# Test User Information

For most users, the password is identical to the username, save for `test1`,
where the password omits the last character of the username.

| Username      | this-is-a-uuid          | this-is-a-differentuuid | not-found-uuid | not-authorized-uuid | in-progress-uuid | failed-uuid | familial-parse-error-uuid |
| ------------- | ----------------------- | ----------------------- | -------------- | ------------------- | ---------------- | ----------- | ------------------------- |
| test1         | ❌                      | ✅                      | ❌             | ❌                  | ✅               | ✅          | ✅                        |
| cefs-mary     | ✅                      | ✅                      | ❌             | ❌                  | ✅               | ✅          | ✅                        |
| cefs-ryan     | ✅                      | ✅                      | ❌             | ❌                  | ✅               | ✅          | ✅                        |
| gf-admin      | ✅                      | ✅                      | ❌             | ❌                  | ✅               | ✅          | ✅                        |
| noaccess      | ❌                      | ❌                      | ❌             | ❌                  | ❌               | ❌          | ❌                        |
| test-center-1 | ✅                      | ❌                      | ❌             | ❌                  | ✅               | ✅          | ❌                        |
| test-center-2 | ✅ (❌ download denied) | ❌                      | ❌             | ❌                  | ✅               | ✅          | ❌                        |
