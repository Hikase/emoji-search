import { UUID } from 'crypto';

export interface ListModel<T> {
  items: T[];
}

export interface Emoji {
  emoji: string;
  name: string;
  shortcode: string;
}

export interface SearchResultModel extends ListModel<Emoji> {
  search_uid: UUID;
}
