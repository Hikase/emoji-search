import { useQuery } from '@siberiacancode/reactuse';

import { Box, CloseButton, Text, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';

import { EmojiList } from '../EmojiList';

interface Emoji {
  emoji: string;
  shortcode: string;
}

interface SearchResult {
  type: string;
  items: Emoji[];
}

const getSearchResult = (query: string) =>
  fetch(`${import.meta.env.VITE_BACKEND_URL}/v1/search?q=${query}`).then((res) =>
    res.json()
  ) as Promise<SearchResult>;

export const EmojiSearch = () => {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      query: '',
    },
  });

  const getSearchQuery = useQuery(() => getSearchResult(form.getValues().query));

  return (
    <>
      <form onSubmit={form.onSubmit(() => getSearchQuery.refetch())}>
        <TextInput
          placeholder="Enter query"
          size="md"
          rightSectionPointerEvents="all"
          leftSection="🔍"
          rightSection={
            <CloseButton
              aria-label="Clear input"
              onClick={() => form.setFieldValue('query', '')}
              style={{ display: form.getValues().query ? undefined : 'none' }}
            />
          }
          key={form.key('query')}
          {...form.getInputProps('query')}
        />
      </form>
      <Box mt="xl">
        {getSearchQuery.data !== undefined &&
          (getSearchQuery.isSuccess ? (
            <EmojiList
              itemsData={getSearchQuery.data.items.map((item) => ({
                emoji: item.emoji,
                emojiName: item.shortcode.replaceAll(':', '').replaceAll('-', ' '),
              }))}
            />
          ) : (
            <Text>No results</Text>
          ))}
      </Box>
    </>
  );
};
