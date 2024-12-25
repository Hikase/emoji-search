import { Container } from '@mantine/core';

import { EmojiSearch } from '@emoji-search/component';

import { Layout } from './Layout';

export const HomePage = () => {
  return (
    <Layout>
      <Container size="md" mt="md">
        <EmojiSearch />
      </Container>
    </Layout>
  );
};
