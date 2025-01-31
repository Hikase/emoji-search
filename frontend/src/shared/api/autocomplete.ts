import { BASE_URL } from './instance';
import { Emoji, ListModel } from './model';

export const getAutocompleteOptions = (query: string) =>
  fetch(`${BASE_URL}/v1/autocomplete?q=${query}`).then((res) => res.json()) as Promise<
    ListModel<Emoji>
  >;
