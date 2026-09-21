# Test Cases

## Authentication
- [ ] Register with valid data creates an account and logs the user in.
- [ ] Register with mismatched passwords is rejected with a clear error.
- [ ] Register with an already-used email is rejected.
- [ ] Login with correct credentials succeeds and returns a JWT.
- [ ] Login with wrong password/email is rejected (401).
- [ ] Logout clears the token and redirects to Home.
- [ ] Visiting a protected page while logged out redirects to Login.

## Questionnaire
- [ ] Age input accepts 10-110 only.
- [ ] Age 15 -> youth-worded questions (school/bullying focus).
- [ ] Age 25 -> young-adult-worded questions (career/finance focus).
- [ ] Age 68 -> older-adult-worded questions (isolation/support focus).
- [ ] Previous/Next navigation works and preserves answers.
- [ ] Submit Assessment is disabled/blocked until the last step.

## Prediction API
- [ ] `POST /api/predictions/predict` with a full payload returns a predicted_label, stress_score, and probabilities.
- [ ] A high-anxiety/low-sleep/low-support payload predicts a higher stress category than a low-anxiety/good-sleep payload.
- [ ] Missing/invalid fields return a 422 validation error, not a silent default.
- [ ] `GET /api/model/metrics` returns real numbers matching `models/metrics.json`.

## Database & History
- [ ] Each prediction is stored in the `assessments` collection with the user's id.
- [ ] `GET /api/predictions/history` returns the user's own assessments only.
- [ ] History table's "View" action opens the correct detail.

## Graphs
- [ ] Analytics page shows "no data" state before any assessment exists.
- [ ] After 1+ assessments, factor bar chart and category pie chart render.
- [ ] After 2+ assessments, the stress-history line chart renders.

## Recommendations
- [ ] Poor sleep answer triggers the sleep-hygiene recommendation.
- [ ] High anxiety answer triggers the breathing/mindfulness recommendation.
- [ ] Reported physical symptoms trigger the "talk to a healthcare professional" recommendation.

## Wellness Assistant
- [ ] A normal message gets a supportive, non-diagnostic reply.
- [ ] A message containing crisis language returns the safety-override message every time.

## Responsiveness & Errors
- [ ] Pages remain usable at a 375px-wide viewport.
- [ ] Backend down / model not trained -> frontend shows a clear error, not a blank crash.
- [ ] Unknown routes render the 404 page.
