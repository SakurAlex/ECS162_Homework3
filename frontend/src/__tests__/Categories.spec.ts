import { test, expect } from 'vitest'
import { render } from '@testing-library/svelte'
import Categories from '../Categories.svelte'

test('Categories renders container', () => {
  // Mount the Categories component with sample props:
  // - `categories`: an array of category names
  // - `activeCategory`: the one that should be highlighted
  const { container } = render(Categories, {
    props: { 
        categories: ['One', 'Two'], 
        activeCategory: 'One' 
    }
  })

  // Assert that the rendered container exists (i.e., component mounted without crashing)
  expect(container).toBeTruthy()
})
