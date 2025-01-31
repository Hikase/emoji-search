import { BASE_URL } from './instance';
import { SearchResultModel } from './model';

export const searchEmoji = (query: string) =>
  fetch(`${BASE_URL}/v1/search?q=${query}`).then((res) => res.json()) as Promise<SearchResultModel>;
