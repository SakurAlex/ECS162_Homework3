// frontend/src/__tests__/Header.spec.ts
import { test, expect } from 'vitest'
import { render, within } from '@testing-library/svelte'
import Header from '../Header.svelte'

test('renders logo and navigation links', () => {
  // Mount Header with sample props for categories and active
  const { container } = render(Header, {
    props: { categories: ['News', 'Sports'], activeCategory: 'News' }
  })

  //Logo check: find the element with id="logo"
  expect(container.querySelector('#logo')).toBeInTheDocument()

  //Navigation scope: find the <nav> element
  const nav = container.querySelector('nav')
  expect(nav).toBeInTheDocument()

  // Create a scoped query API inside <nav>
  const navUtils = within(nav!)
  
  // Now assert only the nav links — no duplicates from elsewhere:
  expect(navUtils.getByText('U.S.')).toBeInTheDocument()
  expect(navUtils.getByText('World')).toBeInTheDocument()
  expect(navUtils.getByText('Business')).toBeInTheDocument()
})
