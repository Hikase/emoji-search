import { UUID } from 'crypto';

import { BASE_URL } from './instance';

export const sendFeedback = (feedback: { searchUid: UUID; emoji: string; rationale: string }) => {
  return fetch(`${BASE_URL}/v1/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      search_uid: feedback.searchUid,
      relevant_emoji: feedback.emoji,
      rationale: feedback.rationale,
    }),
  });
};
