import { useQuery } from '@siberiacancode/reactuse';

import { Box, CloseButton, Text, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';

import { searchEmoji } from '@emoji-search/shared/api/search';

import { EmojiList } from '../EmojiList';
import { FeedbackModal } from '../FeedbackModal';

export const EmojiSearch = () => {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      query: '',
    },
  });

  const searchQuery = useQuery(() => searchEmoji(form.getValues().query));

  const searchResult = searchQuery.data !== undefined ? searchQuery.data.items : [];

  return (
    <>
      <form onSubmit={form.onSubmit(() => searchQuery.refetch())}>
        <TextInput
          placeholder="Enter query"
          size="md"
          rightSectionPointerEvents="all"
          leftSection="🔍"
          rightSection={
            form.getValues().query && (
              <CloseButton
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => form.setFieldValue('query', '')}
                aria-label="Clear value"
              />
            )
          }
          key={form.key('query')}
          {...form.getInputProps('query')}
        />
      </form>
      <FeedbackModal
        suggestedEmoji={searchResult.slice(0, 10)}
        searchUid={searchQuery.data?.search_uid}
      />
      <Box mt="xl">
        {searchQuery.isSuccess ? (
          <EmojiList
            items={searchResult.map((item) => ({
              emoji: item.emoji,
              emojiName: item.name,
            }))}
          />
        ) : (
          <Text>No results</Text>
        )}
      </Box>
    </>
  );
};
